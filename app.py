from flask import (
    Flask,
    render_template,
    request,
    Response,
    redirect,
    url_for,
    jsonify,
    flash,
    session
)

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import csv
import io

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "supersecretkey"

bcrypt = Bcrypt(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

# ==========================
# DATABASE CONFIG
# ==========================

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

db = SQLAlchemy(app)


# ==========================
# DATABASE MODELS
# ==========================

class ReliefRequest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    location = db.Column(
        db.String(100)
    )

    need = db.Column(
        db.String(200)
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# ==========================
# REQUEST HELP
# ==========================

@app.route(
    "/request",
    methods=["GET", "POST"]
)
def request_help():

    if request.method == "POST":

        new_request = ReliefRequest(
            name=request.form["name"],
            location=request.form["location"],
            need=request.form["need"]
        )

        db.session.add(
            new_request
        )

        db.session.commit()

        flash(
            "Request submitted successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "request.html"
    )


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    is_admin = session.get(
        "is_admin",
        False
    )

    location_filter = request.args.get(
        "location"
    )

    need_filter = request.args.get(
        "need"
    )

    query = ReliefRequest.query

    if location_filter:
        query = query.filter(
            ReliefRequest.location
            == location_filter
        )

    if need_filter:
        query = query.filter(
            ReliefRequest.need
            == need_filter
        )

    requests = query.order_by(
        ReliefRequest.id.asc()
    ).all()

    total = ReliefRequest.query.count()

    by_location = db.session.query(
        ReliefRequest.location,
        db.func.count(
            ReliefRequest.id
        )
    ).group_by(
        ReliefRequest.location
    ).all()

    by_need = db.session.query(
        ReliefRequest.need,
        db.func.count(
            ReliefRequest.id
        )
    ).group_by(
        ReliefRequest.need
    ).all()

    return render_template(
        "dashboard.html",
        requests=requests,
        total=total,
        by_location=by_location,
        by_need=by_need,
        location_filter=location_filter,
        need_filter=need_filter,
        is_admin=is_admin
    )


# ==========================
# ADMIN LOGIN
# ==========================

@app.route(
    "/admin_login",
    methods=["POST"]
)
@limiter.limit("5 per minute")
def admin_login():

    username = request.form[
        "username"
    ]

    password = request.form[
        "password"
    ]

    user = User.query.filter_by(
        username=username
    ).first()

    if (
        user and
        user.is_admin and
        bcrypt.check_password_hash(
            user.password,
            password
        )
    ):

        session[
            "username"
        ] = user.username

        session[
            "is_admin"
        ] = True

        flash(
            "Admin login successful!",
            "success"
        )

    else:

        flash(
            "Invalid admin credentials",
            "danger"
        )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# UPDATE STATUS
# ==========================

@app.route(
    "/update_status/<int:request_id>"
)
def update_status(request_id):

    if not session.get(
        "is_admin"
    ):

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    new_status = request.args.get(
        "status"
    )

    req = ReliefRequest.query.get_or_404(
        request_id
    )

    req.status = new_status

    db.session.commit()

    flash(
        "Status updated successfully!",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# EDIT REQUEST
# ==========================

@app.route(
    "/edit_request/<int:request_id>",
    methods=["GET", "POST"]
)
def edit_request(request_id):

    if not session.get(
        "is_admin"
    ):

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    req = ReliefRequest.query.get_or_404(
        request_id
    )

    if request.method == "POST":

        req.name = request.form[
            "name"
        ]

        req.location = request.form[
            "location"
        ]

        req.need = request.form[
            "need"
        ]

        db.session.commit()

        flash(
            "Request updated successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "edit_request.html",
        req=req
    )


# ==========================
# DELETE REQUEST
# ==========================

@app.route(
    "/delete_request/<int:request_id>",
    methods=["POST"]
)
def delete_request(request_id):

    if not session.get(
        "is_admin"
    ):

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    req = ReliefRequest.query.get_or_404(
        request_id
    )

    db.session.delete(req)

    db.session.commit()

    flash(
        "Request deleted successfully!",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# EXPORT CSV
# ==========================

@app.route("/export")
def export():

    if not session.get(
        "is_admin"
    ):

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    location_filter = request.args.get(
        "location"
    )

    need_filter = request.args.get(
        "need"
    )

    query = ReliefRequest.query

    if location_filter:
        query = query.filter(
            ReliefRequest.location
            == location_filter
        )

    if need_filter:
        query = query.filter(
            ReliefRequest.need
            == need_filter
        )

    requests = query.all()

    output = io.StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow([
        "ID",
        "Name",
        "Location",
        "Need",
        "Status"
    ])

    for r in requests:

        writer.writerow([
            r.id,
            r.name,
            r.location,
            r.need,
            r.status
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers[
        "Content-Disposition"
    ] = (
        "attachment;"
        " filename=relief_requests.csv"
    )

    return response


# ==========================
# REGISTER USER
# ==========================

@app.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    existing_user = User.query.filter_by(
        username=data["username"]
    ).first()

    if existing_user:

        return jsonify({
            "msg":
            "Username already exists"
        }), 400

    hashed_pw = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    new_user = User(
        username=data["username"],
        password=hashed_pw,
        is_admin=data.get(
            "is_admin",
            False
        )
    )

    db.session.add(
        new_user
    )

    db.session.commit()

    return jsonify({
        "msg":
        "User registered successfully"
    })


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# CSP
# ==========================

@app.after_request
def apply_csp(response):

    response.headers[
        "Content-Security-Policy"
    ] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' "
        "https://cdn.jsdelivr.net "
        "https://cdnjs.cloudflare.com; "
        "script-src 'self' "
        "'unsafe-inline' "
        "https://cdn.jsdelivr.net; "
        "img-src 'self' data: "
        "https://images.unsplash.com; "
        "font-src 'self' "
        "https://cdnjs.cloudflare.com;"
    )

    return response


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=8501
    )
