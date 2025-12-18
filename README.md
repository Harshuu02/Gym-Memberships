# Gym-Memberships
# 🏋️ Gym Membership Management System (Admin – Phase 1)

A simple **admin-only gym membership management system** built using **Flask + SQLite**.  
This project focuses on managing **members**, **plans**, and **membership assignments** with a clean and modern UI.

> ⚠️ This repository currently contains **Phase 1 (Admin side only)**.  
> Member login and member dashboard will be implemented in later phases.

---

## ✨ Features (Completed)

### ✅ Admin Features
- Add gym members (name, phone)
- Create membership plans (name, duration in days)
- Assign plans to members
- Automatically calculate membership start & end dates
- View members with:
  - Assigned plan
  - Membership status (Active / Expired)
- Clean and modern admin UI
- Separated CSS for maintainability

---

## 🧱 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML + CSS (no JS framework)
- **Version Control:** Git

---

## 🚀 How to Run the Project

### 1️⃣ Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```
### 2️⃣ Install dependencies
```bash
    pip install -r requirements.txt
```
### 3️⃣ Run the app
```bash
    python app.py
```
### 4️⃣ Open in browser
http://127.0.0.1:5000/members



