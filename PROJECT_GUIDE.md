# 🎓 Understanding the Credit Approval System

Welcome! This guide is designed to help you understand how this project works under the hood. It’s perfect for learning the architecture and logic used in professional backend engineering.

---

## 🏗 1. System Architecture

The project follows a **Distributed Architecture**. Here’s why we use these specific components:

### **A. Django (The Web Server)**
Django handles the "Request-Response" cycle. When a user calls an API like `/register`, Django processes the input, speaks to the database, and sends back a JSON response.

### **B. PostgreSQL (The Brain)**
We use a relational database because customer and loan data are highly structured. One customer can have multiple loans (**One-to-Many relationship**).

### **C. Celery & Redis (The Workers)**
When you import 10,000 rows from an Excel file, it takes time. If we do this in the main web server, the app will "freeze" for other users.
- **Celery** is a "worker" that runs tasks in the background.
- **Redis** is the "mailbox" where the web server drops tasks for Celery to pick up later.

---

## 🧠 2. The Credit Scoring Logic (The Algorithm)

The most important part of this project is how we decide if a loan is approved. Here is the exact logic I implemented for you:

### **How the Score (0-100) is Calculated:**
1. **Punctuality (50% weight):** We check what percentage of EMIs were paid on time across all previous loans.
2. **Experience (25% weight):** We count how many loans the user has taken in total.
3. **Current Activity (25% weight):** We check if they have taken too many loans in the current calendar year.

### **The Safety "Kill Switch":**
If a customer’s total debt (sum of all current loans) already exceeds their `Approved Limit`, their score is **automatically set to 0**.

### **Approval Tiers:**
- **Score > 50:** Instant approval.
- **Score 30-50:** Approved, but we increase the interest rate to at least **12%**.
- **Score 10-30:** Approved, but we increase the interest rate to at least **16%**.
- **Score < 10:** Automatic Rejection.

---

## 📊 3. The Local Procedure (The Workflow)

To get this running on your PC, you are essentially creating a virtual mini-network using Docker.

1. **Building Docker Image:** Docker reads the `Dockerfile` to install Python, Linux packages, and our `requirements.txt`.
2. **Migrations:** Django "migrates" the Python models (`Customer`, `Loan`) into actual tables in the PostgreSQL database.
3. **Ingestion Command:** We wrote a custom command `ingest_data` that reads the Excel files using `pandas`, cleans the data, and saves it into the Database.

---

## 🛠 4. Key Files to Study
1. `api/models.py`: Defines the database structure.
2. `api/views.py`: Contains the scoring logic and API responses.
3. `api/tasks.py`: Contains the code for reading Excel in the background.
4. `docker-compose.yml`: Tells Docker how to link the DB, Redis, and Web server together.

---

**Tip:** Try changing the `monthly_income` in a `/register` request and see how it automatically changes the `approved_limit`!
