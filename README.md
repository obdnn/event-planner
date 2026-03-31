# Event Planner API 📅

A robust RESTful API for event management and user registration, built with **Django 6.0** and **Django REST Framework (DRF)**. The project is fully dockerized for a seamless "one-click" launch.

## 🚀 Features

* **User Authentication:** Secure JWT-based authentication (Access & Refresh tokens).
* **Event Management:** Full CRUD operations for events (accessible only to event organizers).
* **Event Registration:** Users can register for events. Includes validation to prevent duplicate registrations and organizer self-registration.
* **Smart Filtering:** Filter upcoming events by date and location.
* **Asynchronous Notifications (Signals):** Automatically sends real-time email notifications upon successful event creation and registration.
* **API Documentation:** Auto-generated interactive Swagger UI and ReDoc.
* **Dockerized:** Ready for development and production with Docker and Docker Compose (MySQL 8.0).

## 🛠️ Tech Stack

* **Backend:** Python 3.13, Django, DRF
* **Database:** MySQL 8.0
* **Auth:** SimpleJWT
* **Containerization:** Docker, Docker Compose
* **API Docs:** drf-spectacular (Swagger UI)

## 🐳 Quick Start (Using Docker)

You don't need to install Python or MySQL locally. Just ensure you have Docker Desktop installed.

**1. Clone the repository:**
```bash
git clone [https://github.com/obdnn/event-planner.git](https://github.com/obdnn/event-planner.git)
cd event-planner
```

**2. Set up environment variables:**
Rename .env.example to .env and fill in your actual credentials (like Gmail App Password):
```bash
cp .env.example .env
```
**3. Build and run the application:**
```bash
docker compose up --build
```
The application will be available at http://127.0.0.1:8000/

**📖 API Documentation**
Once the server is running, you can explore the API endpoints here:

Swagger UI: http://127.0.0.1:8000/api/docs/

ReDoc: http://127.0.0.1:8000/api/redoc/

**👤 Author**
Mykyta Obydennyi