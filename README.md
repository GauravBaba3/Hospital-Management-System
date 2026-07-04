# Hospital Management System

A Django-based web application for managing hospital operations including patient registration, doctor appointments, lab reports, and billing/payments.

## Features

- **Patient Management** — User registration, login, profile management with photo upload
- **Doctor Management** — Browse doctors by speciality, view profiles, book appointments
- **Lab Reports** — Lab technician portal, test ordering, result tracking and dashboard
- **Payments & Discharge** — Discharge summary, final bill generation, payment checkout
- **Google reCAPTCHA** — Form protection on registration/login
- **Static file serving** — WhiteNoise for production-ready static files

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.4 |
| Frontend | Bootstrap 5, crispy-forms |
| Database | SQLite3 |
| Server | Gunicorn |
| Static Files | WhiteNoise |
| Image Processing | Pillow |

## Project Structure

```
learning/
├── learnapp/        # User auth, registration, profile
├── doctors/         # Doctors, treatments, appointments
├── labreports/      # Lab technicians, lab tests, dashboard
├── payments/        # Discharge, billing, payment flow
├── learning/        # Project settings, root URLs
├── templates/       # All HTML templates
├── static/          # CSS, JS, images
├── media/           # Uploaded user/doctor images
└── requirements.txt
```

## Apps & URL Routes

| App | Base URL | Description |
|---|---|---|
| learnapp | `/` | Registration, login, profile |
| doctors | `/doctors/` | Doctor listing, profiles, appointments |
| labreports | `/labreports/` | Lab tech portal, tests, dashboard |
| payments | `/payments/` | Discharge, billing, payment |
| admin | `/admin/` | Django admin panel |

## Setup & Installation

**1. Clone the repository**
```bash
git clone <repo-url>
cd learning
```

**2. Create and activate virtual environment**
```bash
python -m venv env
env\Scripts\activate        # Windows
source env/bin/activate     # Linux/macOS
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```


**5. Apply migrations**
```bash
python manage.py migrate
```

**6. Create a superuser**
```bash
python manage.py createsuperuser
```

**7. Collect static files**
```bash
python manage.py collectstatic
```

**8. Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Data Models

### learnapp
- `UserDetails` — Extends Django's User with phone, address, city, state, zip, profile picture

### doctors
- `DoctorsDetails` — Doctor info with speciality choices (General Medicine, Cardiologist, ENT, Orthopedic, Eye Specialist, Dentist)
- `Treatments` — Treatment linked to a doctor and speciality
- `Appointment` — Patient appointment with doctor, treatment, date, time slot, fee

### labreports
- `LabTechnician` — Staff user with employee ID and qualification
- `LabTests` — Lab test ordered for a patient, referred by a doctor, with result status (Pending / Ongoing / Completed)

### payments
- `Discharge` — Patient discharge record with room type, admission/discharge dates, treatment, and food requirement

## Deployment

The project is configured for deployment on [Render](https://render.com):

- `ALLOWED_HOSTS` includes `.onrender.com`
- WhiteNoise handles static file serving
- Gunicorn is used as the WSGI server

```bash
gunicorn learning.wsgi:application
```

## Dependencies

```
Django==6.0.4
gunicorn==26.0.0
whitenoise==6.12.0
crispy-bootstrap5==2026.3
django-crispy-forms==2.6
django-recaptcha==4.1.0
Pillow==12.2.0
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2026.1
```
