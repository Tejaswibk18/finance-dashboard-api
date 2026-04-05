# 💰 Finance Dashboard Backend API

## 🚀 Overview

This project is a backend system for a **Finance Dashboard** that manages financial records, user roles, and analytics.

It is built using **FastAPI + MongoDB** with **JWT Authentication** and **Role-Based Access Control (RBAC)**.

---

## 🧠 Key Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Secure password hashing (bcrypt)
* Role-based access control (Admin, Analyst, Viewer)

---

### 👤 User Management

* Register and login users
* Role assignment (admin, analyst, viewer)
* Active/inactive user handling

---

### 💰 Financial Records

* Create, update, delete (soft delete)
* Fetch records with filters:

  * type
  * category
  * date
* Pagination support

---

### 📊 Dashboard Analytics

* Total income
* Total expenses
* Net balance
* Category-wise breakdown
* Recent activity
* Monthly & weekly trends (MongoDB aggregation)

---

### ⚙️ Validation & Error Handling

* Strong input validation (Pydantic)
* Custom error responses
* Structured API response format

---

### 🧪 Testing

* Unit tests using pytest
* Covers:

  * Authentication
  * RBAC
  * Validation
  * Edge cases

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Database:** MongoDB
* **Auth:** JWT (python-jose)
* **Validation:** Pydantic v2
* **Testing:** Pytest
* **Password Hashing:** Passlib (bcrypt)

---

## 📁 Project Structure

```
app/
├── main.py
├── core/
├── db/
├── models/
├── schemas/
├── routes/
├── services/
├── auth/
├── utils/
tests/
.env
requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd finance-dashboard-api
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Setup environment variables

Create `.env` file:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=finance_db

JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 5. Run the server

```
uvicorn app.main:app --reload
```

---

## 📌 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Roles & Permissions

| Role    | Permissions                    |
| ------- | ------------------------------ |
| Admin   | Full access (CRUD + dashboard) |
| Analyst | Read + dashboard analytics     |
| Viewer  | Read-only access               |

---

## 📊 Sample APIs

### Auth

* `POST /auth/register`
* `POST /auth/login`

### Records

* `POST /records` (Admin)
* `GET /records`
* `PUT /records/{id}`
* `DELETE /records/{id}` (Soft delete)

### Dashboard

* `GET /dashboard/summary`
* `GET /dashboard/category`
* `GET /dashboard/recent`
* `GET /dashboard/trends?group_by=monthly`

---

## 🧠 Design Decisions

* Used **service layer architecture** to separate logic
* Implemented **RBAC using dependency injection**
* Used **MongoDB aggregation** for analytics
* Implemented **soft delete** for data safety
* Added **pagination** for scalability

---

## 🚀 Optional Enhancements Implemented

* JWT Authentication ✅
* Pagination ✅
* Soft Delete ✅
* Unit Testing ✅
* API Documentation (Swagger) ✅

---

## 📌 Future Improvements

* Rate limiting
* Advanced search
* Role management UI
* Caching for analytics

---

## 🏆 Conclusion

This project demonstrates:

* Clean backend architecture
* Secure authentication & authorization
* Scalable data handling
* Real-world API design

---

## 👨‍💻 Author

**Tejaswi BK**

---
