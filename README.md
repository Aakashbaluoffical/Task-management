# 🚀 Task Management API

A fully-featured **Task Management System API** built with **Django REST Framework**, implementing **JWT Authentication** and **Role-Based Access Control** for users like `superadmin`, `admin`, and `user`.

---

## 📌 Table of Contents

- [📌 Table of Contents](#-table-of-contents)
- [📖 About](#-about)
- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
  


---

## 📖 About

This project provides a backend API for managing tasks across different user roles with permission levels. The main entities are `Users` and `Tasks`, where:

- `Superadmin` can fully control all tasks.
- `Admin` can view all tasks and partially update a few fields.
- `User` can only view and update tasks assigned to them.

---

## ✨ Features

✅ JWT Authentication  
✅ Role-Based Permissions  
✅ Soft Delete Support  
✅ Modular Django App Structure  
✅ Task CRUD with Filtering  

---

## 🛠 Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- SimpleJWT (for authentication)
- PostgreSQL or SQLite
  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/task-api.git
cd task-api
