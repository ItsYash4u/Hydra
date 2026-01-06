# Greeva - Hydroponics Management System

A comprehensive, Django-based web application for monitoring and managing hydroponic farms. This system provides real-time insights into device health, environmental conditions (temperature, pH, humidity), and automated alerts.

## 🚀 Tech Stack

*   **Backend Framework**: Django 5.0+ (Python)
*   **Database**: SQLite (Development), PostgreSQL (Production ready)
*   **Frontend**: Django Templates, Bootstrap 5 (Greeva Admin Theme)
*   **Charts & Maps**: ApexCharts.js, Leaflet.js
*   **Authentication**: django-allauth (Email-based login)
*   **API**: Django Rest Framework (DRF)
*   **Task Queue**: Celery (Configured but optional for basic usage)

## 📂 Project Structure

```
Greeva/
├── config/                 # Project configuration (Settings, URLs, WSGI/ASGI)
│   ├── settings/           # Split settings (base, local, production)
│   └── urls.py             # Main URL routing
├── greeva/                 # Main application source code
│   ├── hydroponics/        # Core domain logic (Devices, Sensors, Alerts)
│   ├── pages/              # General views (Dashboard, Static pages)
│   ├── users/              # Custom User model & Auth logic
│   ├── templates/          # HTML Templates (extends base.html/vertical.html)
│   └── static/             # CSS, JS, Images
├── requirements/           # Python dependencies
└── manage.py               # Django management script
```

## ✨ Features

*   **Dashboard**: Centralized view of farm health, active alerts, and sensor averages.
*   **Device Management**: Register and monitor status (Online/Offline) of greenhouses and tanks.
*   **Sensor Monitoring**: Track Temperature, pH, Humidity, Moisture, Light, and Conductivity.
*   **Alert System**: Automated alerts for threshold breaches (e.g., "High Temperature").
*   **Interactive Maps**: Visualize device locations on a global map.
*   **User Management**: Role-based access (Admin, Operator) with email authentication.

## 🛠️ Setup & Installation

### Prerequisites
*   Python 3.10+
*   pip (Python package manager)

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd Greeva
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements/local.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory (copy from `.env.example` if available) or use the defaults in `settings/base.py`.

5.  **Apply Database Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser** (for Admin access)
    ```bash
    python manage.py createsuperuser
    ```

## 🏃‍♂️ How to Run

### Development Server
```bash
python manage.py runserver
```
Access the dashboard at: **http://127.0.0.1:8000/**

### Generating Sample Data
To quickly populate the dashboard with realistic test data:
```bash
python manage.py generate_data
```
*This creates an admin user (`admin@example.com` / `password`) and sample devices/readings.*

## 🧪 Running Tests

To run the test suite:
```bash
pytest
```

## 🔮 Future Work / TODOs

*   **Real-time WebSockets**: Re-enable Django Channels for live sensor updates (currently disabled).
*   **API Authentication**: Implement JWT for external IoT device communication.
*   **Mobile App**: Build a React Native companion app using the DRF APIs.
