# 🚀 Task Management Application with Task Completion Report

Task Management System API built with **Django** and **Django REST Framework**. implementing **JWT Authentication** and **Role-Based Access Control** for users like `superadmin`, `admin`, and `user` ,**soft delete**, and a **custom admin panel**. Users log hours and submit reports when completing tasks.


---

## 📌 Table of Contents

- [📌 Table of Contents](#-table-of-contents)
- [📖 About](#-about)
- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
  


---

## 📖 About

A full-stack task management system built with Django and Django REST Framework. It includes role-based user access, JWT authentication, soft delete, and a custom admin panel. Users can submit reports and log hours when completing tasks for better transparency and accountability.

- `Superadmin` can fully control all tasks.
- `Admin` can view all tasks and partially update a few fields.
- `User` can only view and update tasks assigned to them.

---

## ✨ Features

✅ JWT Authentication using SimpleJWT
✅ Role-Based Access (SuperAdmin, Admin, User)
✅ Task CRUD with Filtering
✅ Completion Report and Worked Hours Submission
✅ Soft Delete Support
✅ Custom HTML Admin Panel
✅ Pagination Support
✅ Modular Django App Structure 

---

## 🛠 Tech Stack

- Backend: Python 3.10+, Django 4.x, Django REST Framework, SimpleJWT (for authentication)
- Frontend: HTML, Bootstrap
- Database: SQLite (default), PostgreSQL (optional)
- Others: Django Templates, Custom Middleware
  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Aakashbaluoffical/Task-management.git
cd TaskManagement
```
### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
   pip install -r requirements.txt
```
### 4. Apply Migrations
```bash
python manage.py migrate
```
### 5. Create Superuser (for SuperAdmin Access)
```bash
python manage.py createsuperuser
```
### 6. Run the Server
```bash
python manage.py runserver
```
## 🚀 How to Use

✅ As a SuperAdmin:
- Login to the custom admin panel (/admin-panel/)
- Create Admin and User accounts
- Assign users to Admins
- View/manage all tasks and reports

✅ As an Admin:
- Login to the admin panel
- Assign tasks to users
- View task status and reports

✅ As a User:
- Login via API using JWT token
- View assigned tasks
- Submit completion reports and worked hours upon finishing tasks

## 🔐 API Authentication (JWT)

- Login Endpoint: `/api/v1/user/token/`
  - Use username and password to receive access and refresh tokens.
- Token Refresh: `/api/v1/user/token/refresh`

Include Authorization: `Bearer <access_token>` in the header for authenticated requests.

## 📌 Core API Endpoints
Method	Endpoint	Description
GET	 - /tasks/	Fetch tasks assigned to the user
PUT	/tasks/{id}/	Update task status (mark as completed)
GET	/tasks/{id}/report/	View report (admin & superadmin only)

| Method | Endpoint                  | Description                                     |
|--------|---------------------------|-------------------------------------------------|
| POST   | api/v1/user/register      | Register a new user                             |
| GET    | api/v1/tasks/             | List all tasks (based on user role)             |
| POST   | api/v1/tasks/             | Create a new task (admin/superadmin only)       |
| GET    | api/v1/tasks/121          | Retrieve details of a specific task             |
| PUT    | api/v1/tasks/121          | Fully update a specific task (superadmin only)  |
| PATCH  | api/v1/tasks/121          | Partially update task status/report/hours       |
| GET    | api/v1/tasks/121/report   | View task completion report and worked hours    |

