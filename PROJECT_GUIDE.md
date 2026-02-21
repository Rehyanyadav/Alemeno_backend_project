# 🎓 Credit Approval System - Professional Engineering Guide

This guide describes the architecture, logic, and operational procedures of the Credit Approval System. It is designed to demonstrate professional backend engineering practices, including distributed tasks, relational modeling, and automated data processing.

---

## 🏗 1. System Architecture
The project is built on a **Distributed Multi-Service Architecture** orchestrated via Docker.

### **Components:**
*   **Django (Web Server):** Handles the RESTful API and core business logic.
*   **PostgreSQL (Database):** A relational database storing structured Customer and Loan records with high integrity.
*   **Celery (Worker):** Handles heavy lifting, such as Excel data ingestion, without blocking the main web server.
*   **Redis (Message Broker):** Acts as the communication bridge between Django and the Celery workers.
*   **Docker:** Ensures the environment is identical across all machines (Database, Redis, and App).

---

## 🧠 2. The Credit Scoring Algorithm (The Heart of the System)
The credit score (0-100) determines whether a loan is approved and at what interest rate.

### **The Weighting (50/25/25 Rule):**
1.  **Punctuality (50%):** Calculated as the ratio of `EMIs paid on time` vs `Total EMIs` across all historical loans.
2.  **Experience (25%):** Rewards users for having taken multiple loans. (5 points per loan, capped at 25).
3.  **Active Activity (25%):** Penalizes users who have taken too many loans in the current calendar year. (Starts at 25 points, decreases for every new loan).

### **The Safety Kill-Switches:**
*   **Debt-to-Limit Ratio:** If a customer's total **Current Debt** (active loans) exceeds their `Approved Limit`, their score is automatically set to **0**.
*   **Income Burden:** If the total monthly EMIs (existing + new) exceed **50% of the customer's monthly income**, the loan is automatically rejected, regardless of the score.

---

## 🛠 3. Setup & Operations

### **Step 1: Start the Environment**
```bash
docker-compose up -d --build
```

### **Step 2: Database Setup**
Apply migrations to create the tables in PostgreSQL:
```bash
docker-compose exec web python manage.py makemigrations api
docker-compose exec web python manage.py migrate
```

### **Step 3: Data Ingestion**
Import the `customer_data.xlsx` and `loan_data.xlsx` into the database:
```bash
docker-compose exec web python manage.py ingest_data
```

### **Step 4: Create Admin Access**
To view data via the web interface:
```bash
docker-compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```
*   **Admin Login:** `http://localhost:8000/admin/` (User: `admin`, Pass: `admin123`)

---

## 📊 4. API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/` | GET | Index showing all available endpoints. |
| `/api/register/` | POST | Registers a customer and calculates their limit. |
| `/api/check-eligibility/`| POST | Checks if a loan is approved and returns interest rate. |
| `/api/create-loan/` | POST | Finalizes and saves an approved loan. |
| `/api/view-loan/<id>/` | GET | Fetches full details of a specific loan. |
| `/api/view-loans/<id>/`| GET | Lists all historical and active loans for a customer. |

---

## 🧪 5. Testing & Validation
We use Django's testing suite to verify the logic. To run the automated tests:
```bash
docker-compose exec web python manage.py test api
```

---

## � Key Files to Study
1.  `api/models.py`: Defines the database schema (ForeignKeys, AutoFields).
2.  `api/views.py`: Contains the complex math for Credit Scoring and Eligibility.
3.  `api/tasks.py`: Demonstrates background processing with Pandas.
4.  `api/admin.py`: Configures the advanced search and filter views in the Admin panel.
5.  `docker-compose.yml`: Defines the infrastructure (DB, Redis, Worker).

---
**Note:** This system follows the strict requirements of the Backend Assignment while adding industrial-grade safety checks and documentation.
