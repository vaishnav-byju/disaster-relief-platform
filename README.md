# 🚀 Smart Disaster Relief Coordination Platform

### Cloud-Based Secure Web Application (DevSecOps Project)

---

## 📌 Overview

The **Smart Disaster Relief Coordination Platform** is a cloud-native, secure web application designed to coordinate disaster relief operations efficiently using **AWS Cloud and DevSecOps practices**.

The system focuses on:

* Secure application design
* Scalable cloud architecture
* Automated deployment (CI/CD)
* Monitoring and logging
* Role-based access control

---

## 🎯 Key Objectives

* Build a full-stack web application with role-based access
* Deploy on AWS using secure infrastructure design
* Implement DevSecOps pipeline using CI/CD automation
* Ensure security best practices (authentication, hashing, HTTPS, etc.)
* Monitor system health using CloudWatch

---

## 🧰 Tech Stack

**Backend**

* Python (Flask)

**Frontend**

* HTML, CSS, JavaScript

**Database**

* AWS RDS (MySQL)

**Cloud & Deployment**

* AWS EC2
* AWS S3
* Docker
* NGINX (Reverse Proxy)

**DevOps Tools**

* Git & GitHub
* GitHub Actions / Jenkins (CI/CD)
* Docker

**Monitoring**

* AWS CloudWatch (Metrics + Logs)

---

## 🏗️ System Architecture

The system follows a **3-tier cloud architecture**:

* **Frontend Layer** → User Interface (HTML/CSS)
* **Application Layer** → Flask backend running on EC2 (Dockerized)
* **Database Layer** → AWS RDS MySQL

### Supporting Components:

* S3 → Media & backup storage
* CloudWatch → Monitoring & alerts
* NGINX → Reverse proxy
* IAM → Secure access control

---

## 🔐 Security Implementation

This project follows key cybersecurity principles:

### Authentication & Authorization

* Role-Based Access Control (Admin / User / Volunteer)
* Secure login system

### Data Security

* Password hashing using bcrypt/secure hashing methods
* SQL Injection prevention using parameterized queries

### Web Security

* Protection against XSS (input sanitization)
* Security headers (CSP, X-Frame-Options, etc.)
* HTTPS enforcement using SSL/TLS

### Infrastructure Security

* AWS Security Groups (least privilege access)
* Private subnets for backend systems
* SSH hardening and key-based authentication
* Fail2Ban for brute-force protection

---

## ⚙️ CI/CD Pipeline

The project uses an automated CI/CD pipeline to ensure continuous deployment.

### Pipeline Flow:

1. Code pushed to GitHub
2. GitHub Actions / Jenkins triggers pipeline
3. Docker image is built
4. Application is deployed to EC2 instance
5. Container is restarted automatically

### Benefits:

* Faster deployments
* Reduced manual errors
* Consistent production builds

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t relief-app .
```

### Run Container

```bash
docker run -d -p 5000:5000 --name relief-container relief-app
```

### Stop Container

```bash
docker stop relief-container
```

---

## ☁️ AWS Infrastructure

### Components Used:

* **EC2** → Application hosting
* **VPC** → Isolated network environment
* **Subnets** → Public & private segmentation
* **RDS** → Managed database
* **S3** → File storage & backups
* **CloudWatch** → Monitoring & logging

---

## 📊 Monitoring & Logging

* CloudWatch metrics for CPU, memory, and disk usage
* Application logs stored and monitored
* Alerts configured for:

  * High CPU usage
  * Failed login attempts
  * System errors

---

## 📂 Project Structure

```
disaster-relief-platform/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── backup.sh
├── nginx_full.txt
│
├── templates/
├── static/
│
├── docs/
│   ├── architecture-diagram.png
│   ├── security-documentation.pdf
│   ├── screenshots/
│
├── .github/workflows/
└── README.md
```

---

## 🚀 Deployment Summary

1. EC2 instance launched (Ubuntu)
2. Docker installed and configured
3. Flask app containerized
4. NGINX configured as reverse proxy
5. Application deployed and exposed via port mapping
6. CI/CD pipeline automates updates

---

## 📌 Future Improvements

* Add AWS WAF for advanced protection
* Implement CloudFront CDN
* Add Terraform (Infrastructure as Code)
* Enable multi-region disaster recovery
* Add automated vulnerability scanning (SAST/DAST)

---

## 📚 References

* [https://docs.aws.amazon.com](https://docs.aws.amazon.com)
* [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
* [https://docs.docker.com](https://docs.docker.com)
* [https://docs.github.com/en/actions](https://docs.github.com/en/actions)
* [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* [https://certbot.eff.org](https://certbot.eff.org)

---

## 👨‍💻 Author
Vaishnav Byju
BCA – Marian College Kuttikanam Autonomous
