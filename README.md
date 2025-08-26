# Academic Score Tracker (API) 🎓📊

A Django + DRF powered API designed to help students track their academic performance across semesters.  
It records courses, grades, and units, then automatically computes GPA and CGPA.  

🚀 Built by **Adedotun (Hon. Triple A)** as part of my ALX Backend Capstone Project.  
This project reflects my passion for building real-world backend systems that solve practical problems students face.  

## 🌟 Features

- User authentication (Register, Login, Token-based access)  
- Create and manage semesters  
- Add, update, and delete courses  
- Automatic GPA and CGPA calculation per user  
- Secure API endpoints using Django REST Framework  


## ⚡ Quickstart

```bash
git clone https://github.com/<your-username>/academic-score-tracker.git
cd academic-score-tracker

# Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt # optional if requirements.txt exists
pip install django djangorestframework djangorestframework-authtoken

# Setup database
python manage.py migrate

# Run server
python manage.py runserver



🔑 Authentication

Register
POST /api/auth/register/
Payload: { "username": "demo", "email": "demo@mail.com", "password": "password123" }

Get Token
POST /api/auth/token/
Payload: { "username": "demo", "password": "password123" }
Response: {"token": "..."}


🔒 Use header in requests:

Authorization: Token <token>



📌 Endpoints

Semesters

GET/POST /api/semesters/

GET/PUT/PATCH/DELETE /api/semesters/{id}/


Courses

GET/POST /api/courses/

GET/PUT/PATCH/DELETE /api/courses/{id}/


Summary

GET /api/summary/ → { "cgpa": ..., "totals": ... }




---

✨ Vision

This project is a starting point for a larger idea:
helping students see their academic journey at a glance, stay motivated, and plan ahead with accurate performance data.



🧑‍💻 Author

Adedotun (Hon. Triple A)

Student of Materials Science & Engineering, Obafemi Awolowo University

Backend Developer (Python/Django, DRF)

Tech enthusiast, passionate about solving real-world problems through software




📬 Contributions & Feedback

This is a learning project — I’d love to hear your feedback, ideas, or contributions!