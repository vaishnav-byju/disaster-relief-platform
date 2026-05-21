# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app source code
COPY . .

# Expose Flask port
EXPOSE 8501

# Run the app
CMD ["python", "app.py"]
