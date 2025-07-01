# AtkinsRéalis Secure Booking Application

This Django-based internal booking system was developed to demonstrate secure web development practices aligned with the OWASP Top 10 (2024).

## Features

- CSRF protection on all POST forms
- Strong password enforcement
- Login attempt lockout after repeated failures
- Hidden admin URL with warning trap
- Secure session handling via Django auth

## OWASP Protections

- A01:2024 – Broken Access Control (CSRF)
- A05:2024 – Security Misconfiguration (admin URL)
- A07:2024 – Authentication Failures (password/lockout)

## How to Run

```bash
git clone https://github.com/yourusername/atkinsrealis-booking-app.git
cd atkinsrealis-booking-app
python -m venv venv
source venv/bin/activate       # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
