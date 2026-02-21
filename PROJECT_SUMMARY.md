# 📊 Credit Approval System - Project Summary

This project is a robust backend solution for a Credit Approval System, built as part of a Backend Internship Assignment. It automates the process of customer registration, credit score calculation, and loan eligibility assessment using modern backend technologies.

## 🛠 Tech Stack
- **Framework:** Django 4.2 & Django REST Framework (DRF)
- **Database:** PostgreSQL (Relational storage)
- **Task Queue:** Celery (Background workers)
- **Broker:** Redis (Message broker for Celery)
- **Containerization:** Docker & Docker Compose
- **Data Handling:** Pandas (Excel ingestion)

---

## ✅ Implementation Checklist

| Feature | Status | Details |
| :--- | :--- | :--- |
| **Setup & Config** | ✅ Completed | Django project initialized with environment-based configuration. |
| **Data Models** | ✅ Completed | `Customer` and `Loan` models designed for optimal queries. |
| **Dockerization** | ✅ Completed | Full orchestration of App, DB, Redis, and Worker services. |
| **Background Ingestion** | ✅ Completed | Automated import of `customer_data.xlsx` and `loan_data.xlsx`. |
| **Credit Scoring Engine**| ✅ Completed | Logic for internal credit rating (0-100) based on historical data. |
| **API /register** | ✅ Completed | Registers user and calculates 36x salary credit limit. |
| **API /check-eligibility**| ✅ Completed | Predictive endpoint checking approval and adjusting interest rates. |
| **API /create-loan** | ✅ Completed | Processes approval and persists the loan to the database. |
| **API /view-loan** | ✅ Completed | Fetches specific loan details with nested customer profile. |
| **API /view-loans** | ✅ Completed | Lists all active loans for a specific customer. |

---

## 🚀 Deployment Overview
The project is built to be "Single-Command Deployment." By using `docker-compose up --build`, all dependencies are automatically provisioned and linked.

1. **Build:** `docker-compose up --build`
2. **Setup:** `docker-compose exec web python manage.py migrate`
3. **Ingest:** `docker-compose exec web python manage.py ingest_data`

---

## 📈 Future Enhancements
- **Unit Tests:** Adding more code coverage for the scoring algorithm.
- **Frontend Dashboard:** A simple UI for loan officers to review applications.
- **Authentication:** Securing endpoints using JWT or Session-based auth.
