# 📆Maktabiya - Desk Booking App

<div align="center">
    <img alt="MaktabiyaLogo" src="/maktabiya/maktabiya-app/app_core/static/app_core/img/logo.png" width="400">
</div>

![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)
![Maktabiya](https://img.shields.io/badge/Maktabiya_version-1.2.3-lightgreen?style=for-the-badge)
![Django](https://img.shields.io/badge/django-5.2.11-darkgreen?style=for-the-badge)
![Django-Q2](https://img.shields.io/badge/django_q2-1.9.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge)
![PyConTalkDE](https://img.shields.io/badge/PyCon-DE_2026-orange?style=for-the-badge)

A modern, scalable desk booking application built with Django. Maktabiya enables organizations to efficiently manage shared office spaces, book desks, and optimize workspace utilization with real-time availability, automated notifications, and a user-friendly interface.

> **Note**: This is a demo application used for PyCon DE 2026 talk **"Django-Q2: Async Tasks Made Simple"**.  
> Perfect for learning Django best practices, background task processing, and building scalable web applications.

---

## 📖 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture-overview)
- [Quick Start](#-quick-start)
- [Installation & Setup](#-installation--setup)
- [Usage & Workflows](#-usage)
- [Management Commands](#️-management-commands)
- [Configuration](#️-configuration)
- [Docker Commands](#-docker-commands-reference)
- [Project Structure](#-project-structure)
- [Database Migrations](#-database-migrations)
- [Security](#-security-considerations)
- [Development Tips](#-development-tips)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🎯 Features

- 🏢 **Desk Management**: Create and manage office spaces and desk configurations
- 📅 **Booking System**: Intuitive booking interface with real-time availability tracking
- 👤 **User Authentication**: Secure user registration and login system
- 📧 **Email Notifications**: Automated booking confirmations, reminders, and reports
- 🎨 **Admin Dashboard**: Comprehensive admin interface using Django Jazzmin
- ⚙️ **Background Tasks**: Asynchronous task processing with Django Q2
- 🏢 **Multi-Office Support**: Support for multiple offices and booking zones
- 📊 **Analytics**: Monthly reporting and usage statistics
- 📱 **Responsive Design**: Mobile-friendly user interface
- 🔔 **Automated Workflows**: Scheduled tasks for reminders and report generation

## 🏗️ Architecture Overview

### Application Components

```bash
Maktabiya Desk Booking System
├── app_core/           # Core application logic and configuration
├── booking/            # Booking management and workflows
├── email_templates/    # Email notification templates
├── user/               # User authentication and profiles
├── maktabiya/          # Django project settings
```

### Technology Stack

| Component | Technology | Version |
| --------- | --------- | ------- |
| **Web Framework** | Django | 5.2.11 |
| **Language** | Python | 3.12+ |
| **Database** | PostgreSQL | 17 |
| **Task Queue** | Django Q2 | 1.9.0 |
| **Admin Panel** | Django Jazzmin | 3.0.1 |
| **Email Testing** | Mailpit | v1.29.2 |
| **Containerization** | Docker | 29+ |
| **Orchestration** | Docker Compose | v5+ |

## 📋 Prerequisites

Before running Maktabiya, ensure you have the following installed:

- **Docker** (version 29 or higher)
- **Docker Compose** (version v5 or higher)
- **Git** (for cloning the repository)

For local development without Docker:

- **Python** 3.12 or higher
- **PostgreSQL** 17 or higher

## ⚡ Quick Start

Get Maktabiya running in 3 minutes:

```bash
# 1. Clone the repository
git clone <repository-url>
cd pycon-de-2026/maktabiya

# 2. Copy environment configuration
cp env.sample .env

# 3. Start with Docker Compose
docker compose up -d --build

# 4. Access the application
#    - Web App:    http://localhost:8000
#    - Admin:      http://localhost:8000/admin
#    - Mailpit:    http://localhost:8025

# Default credentials: admin / admin
```

That's it! Your desk booking system is ready to use.

## 🚀 Installation & Setup

### Option 1: Running with Docker Compose (Recommended)

Docker Compose will handle all services including the database, app, mail server, and background task workers.

#### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd maktabiya
```

#### Step 2: Configure Environment Variables

Copy the sample environment file and update variables as needed:

```bash
cp env.sample .env
```

set True to have some demo data set up

```bash
CREATE_DEMO_DATA=True
```

#### Step 3: Build and Run

```bash
docker compose up -d --build
```

This command will:

- Build the Docker image for the Maktabiya app
- Start PostgreSQL database container
- Start the Django application container
- Start the Mailpit email server
- Start the background task worker(s)

#### Step 4: Verify Services

Check that all services are running:

```bash
docker compose ps
```

Expected output:

```bash
NAME                 STATUS      PORTS
maktabiya-db         Up (healthy)  127.0.0.1:5432->5432/tcp
maktabiya-app        Up (healthy)  0.0.0.0:8000->8000/tcp
maktabiya-mail-server Up           0.0.0.0:1025->1025/tcp, 0.0.0.0:8025->8025/tcp
maktabiya-tasks-1     Up            
```

### Option 2: Local Development Setup

For local development without Docker:

#### Step 1: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
cd maktabiya-app
pip install -r requirements.txt
```

#### Step 3: Configure Environment

```bash
cp ../env.sample ../.env
```

#### Step 4: Set Up Database

Ensure PostgreSQL is running locally, then:

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### Step 5: Run the Application

```bash
python manage.py runserver 0.0.0.0:8000
```

## 🔧 Usage

### Accessing the Application

Once running, access Maktabiya at:

- **Main Application**: <http://localhost:8000>
- **Admin Dashboard**: <http://localhost:8000/admin>
- **Mailpit UI**: <http://localhost:8025> (email server interface)

### Default Credentials

Default admin credentials (from `env.sample`):

- **Username**: `admin`
- **Email**: `admin@AladinStudioX.app`
- **Password**: `admin`

⚠️ **Security Note**: Always Change default credentials immediately in production!

### Core Application Workflows

#### 1. Create an Office

- Log in to the admin dashboard
- Navigate to **Offices** section
- Add a new office with name and location
- Create rooms within the office
- Configure available desks per room

#### 2. Browse and Book a Desk

- Log in as a regular user
- Navigate to the booking page
- Select a date and available desk
- Confirm the booking
- Receive confirmation email via Mailpit

#### 3. View and Manage Bookings

- Users can view all their bookings via "My Bookings" page
- Cancel bookings before the scheduled date
- Managers can view team bookings

#### 4. Automated Workflows

- Monthly reports generated automatically
- Email reminders sent before booking date
- Task workers process background jobs asynchronously

## 🛠️ Management Commands

Maktabiya provides custom Django management commands for common tasks. Use them with the following syntax:

```bash
# Via Docker
docker compose exec app python manage.py <command> [options]

# Local development
python manage.py <command> [options]
```

### Available Commands

#### 1. `setup_workspace` - Create Office Infrastructure

Provisions a new office with rooms and desks.

**Usage:**

```bash
docker compose exec app python manage.py setup_workspace "Office Name" [options]
```

**Options:**

- `--rooms N` - Number of rooms to create (default: 1)
- `--desks N` - Number of desks per room (default: 4)

**Examples:**

```bash
# Create an office with 1 room and 4 desks
docker compose exec app python manage.py setup_workspace "Dhaka Office"

# Create an office with 3 rooms, 6 desks each
docker compose exec app python manage.py setup_workspace "Rome Office" --rooms 3 --desks 6
```

---

#### 2. `seed_bookings` - Generate Demo Bookings

Populates the database with realistic booking data for testing and demonstrations.

**Usage:**

```bash
docker compose exec app python manage.py seed_bookings [options]
```

**Options:**

- `--user-count N` - Number of users to create (default: 10)
- `--office NAME` - Specific office to book in (default: all offices)
- `--bookings-per-day N` - Target bookings per day (default: 5)
- `--manager-email EMAIL` - Assign bookings to a specific manager

**Examples:**

```bash
# Generate 10 users with 5 bookings per day
docker compose exec app python manage.py seed_bookings

# Create 20 users for Dhaka office only
docker compose exec app python manage.py seed_bookings --user-count 20 --office "Dhaka Office"

# Assign bookings to a manager
docker compose exec app python manage.py seed_bookings --manager-email "manager@AladinStudioX.app"
```

---

#### 3. `add_tasks` - Benchmark Background Tasks

Adds tasks to the queue for testing Django Q2 task workers and measuring dispatch/execution times.

**Usage:**

```bash
docker compose exec app python manage.py add_tasks [count] [options]
```

**Options:**

- `count` - Number of tasks to add (default: 100)
- `--qcluster NAME` - Target queue cluster (default: DefaultQueue)

**Examples:**

```bash
# Add 100 tasks to the default queue
docker compose exec app python manage.py add_tasks 100

# Add 500 tasks to a specific queue for benchmarking
docker compose exec app python manage.py add_tasks 500 --qcluster LongTasks
```

**Notes:**

- Tasks are email sending operations, viewable in Mailpit (<http://localhost:8025>)
- Monitor task processing in real-time via the Django Q2 dashboard
- Useful for testing worker performance and scaling

---

#### 4. `check_user_exists` - Verify User Existence

Checks if a user exists in the database.

**Usage:**

```bash
docker compose exec app python manage.py check_user_exists <username>
```

**Examples:**

```bash
# Check if user exists
docker compose exec app python manage.py check_user_exists admin

# Returns exit code 0 if exists, 1 if not found
```

---

#### 5. Standard Django Commands

All standard Django commands are available:

```bash
# Create a new superuser
docker compose exec app python manage.py createsuperuser

# Run database migrations
docker compose exec app python manage.py migrate

# Create migration files
docker compose exec app python manage.py makemigrations

# Check migration status
docker compose exec app python manage.py showmigrations

# Access Django shell
docker compose exec app python manage.py shell

# Collect static files
docker compose exec app python manage.py collectstatic --noinput
```

---

### Management Command Examples - Real Scenarios

### Scenario 1: New Demo Setup

```bash
# 1. Create multiple offices
docker compose exec app python manage.py setup_workspace "Dhaka" --rooms 2 --desks 10
docker compose exec app python manage.py setup_workspace "Rome" --rooms 3 --desks 8

# 2. Populate with booking data
docker compose exec app python manage.py seed_bookings --user-count 20 --bookings-per-day 8

# 3. Add test tasks
docker compose exec app python manage.py add_tasks 50
```

### Scenario 2: Performance Testing

```bash
# Test with different queue clusters
docker compose exec app python manage.py add_tasks 1000 --qcluster DefaultTasks
docker compose exec app python manage.py add_tasks 1000 --qcluster LongTasks
```

## ⚙️ Configuration

### Environment Variables

Key configuration variables in `.env`:

```dotenv
# App settings
APP_DOMAIN=localhost:8000
APP_VERSION=1.2.3
MYBOOK_URL=my-bookings
DEBUG=False
LOGLEVEL=INFO
SECRET_KEY="Maktabiya-AladinStudioX"
ALLOWED_HOSTS=*
INTERNAL_IPS=127.0.0.1
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
USE_TZ=True
USER_APP_LOG_LEVEL=INFO
DJANGO_APP_LOG_LEVEL=ERROR

# Admin Settings
CREATE_DEFAULT_ADMIN=True
DJANGO_SUPERUSER_EMAIL=admin@AladinStudioX.app
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_USERNAME=admin 

# DataBase SETTINGS
DB_ENGINE=postgres
DB_HOST=maktabiya-db
DB_NAME=maktabiya
DB_USERNAME=maktabiya
DB_PASS=maktabiya
DB_PORT=5432
# seconds unit
DB_CHECK_SLEEP_DURATION=900

# EMAIL SETTINGS 
EMAIL_HOST=maktabiya-mail-server
EMAIL_TIMEOUT=10
DEFAULT_FROM_EMAIL=no-reply@AladinStudioX.app
EMAIL_HOST_PASSWORD=
EMAIL_PORT=1025
EMAIL_USE_TLS=False

# Default App Settings
CREATE_DEMO_DATA=True
```

### Database Configuration

Maktabiya uses PostgreSQL. The database is automatically initialized when using Docker Compose. Default credentials in `.env`:

- **User**: `maktabiya`
- **Password**: `maktabiya`
- **Database**: `maktabiya`

### Email Configuration

Mailpit is used for email development/testing. To view emails:

- Open <http://localhost:8025>
- All outgoing emails will appear in the Mailpit UI
- For production, replace `EMAIL_HOST` with your actual SMTP server

### Background Tasks

Maktabiya uses Django Q2 for background task processing:

- **Task Worker**: Runs in a separate container (`maktabiya-tasks-*`)
- **Broker**: Can use different brokers, refere [Django-Q2 docs](https://django-q2.readthedocs.io/en/master/brokers.html)(default: database for Maktabiya)
- **Scheduler**: Handles scheduled tasks like booking reminders and generate report
- **Multiple Worker process**: Can scale horizonatally the worker process
- **Multiple and Separate Task Queues**: Can have different type of queues workers (e.g. long task queues, short task queues)

## 🐳 Docker Commands Reference

### Start and Stop Services

**Start services (build and start in background):**

```bash
docker compose up -d --build
```

**Stop all services:**

```bash
docker compose down
```

**Stop and remove volumes (clean wipe):**

```bash
docker compose down -v
```

**Restart services:**

```bash
docker compose restart
```

### View Logs and Status

**Check service status:**

```bash
docker compose ps
```

**View all logs (follow in real-time):**

```bash
docker compose logs -f
```

**View specific service logs:**

```bash
docker compose logs -f app       # App logs
docker compose logs -f db        # Database logs
docker compose logs -f mail-server  # Mail server logs
docker compose logs -f tasks     # Task worker logs
```

**View last 100 lines:**

```bash
docker compose logs --tail=100 app
```

### Execute Commands in Container

**Run management commands:**

```bash
docker compose exec app python manage.py <command>
```

**Access Django shell:**

```bash
docker compose exec app python manage.py shell_plus
```

**Run Python scripts:**

```bash
docker compose exec app python script.py
```

**Execute shell commands:**

```bash
docker compose exec app bash
```

### Database Operations

**Connect to PostgreSQL:**

```bash
docker compose exec db psql -U maktabiya -d maktabiya
```

**Backup database:**

```bash
docker compose exec db pg_dump -U maktabiya maktabiya > backup.sql
```

**Restore database:**

```bash
docker compose exec -T db psql -U maktabiya maktabiya < backup.sql
```

### Scale and Monitor

**Scale task workers (run N workers):**

```bash
# Edit docker-compose.yml and set replicas value, then:
docker compose up -d
```

**Monitor task queue:**

```bash
docker compose logs -f tasks
```

**Health check status:**

```bash
docker compose ps  # Shows health status for each service
```

## 📁 Project Structure

```bash
maktabiya/
├── maktabiya-app/              # Django application
│   ├── manage.py               # Django management utility
│   ├── requirements.txt         # Python dependencies
│   ├── entrypoint.sh            # Container entry point
│   ├── gunicorn-cfg.py          # Gunicorn configuration
│   │
│   ├── app_core/                # Core app
│   │   ├── models.py            # Core models
│   │   ├── management/          # Custom commands
│   │   └── tasks.py             # Background tasks
│   │
│   ├── booking/                 # Booking module
│   │   ├── models.py            # Booking models
│   │   ├── views.py             # Booking logic
│   │   ├── forms.py             # Booking forms
│   │   └── templates/           # Booking templates
│   │
│   ├── user/                    # User authentication
│   │   ├── models.py            # User models
│   │   ├── forms.py             # User forms
│   │   └── templates/           # User templates
│   │
│   ├── email_templates/         # Email templates
│   │   └── templates/emails/    # HTML email templates
│   │
│   └── maktabiya/               # Project settings
│       ├── settings/            # Settings components
│       ├── urls.py              # URL routing
│       ├── wsgi.py              # WSGI config
│       └── asgi.py              # ASGI config
│
├── db/                          # Database configuration
│   └── server.json              # DB connection info
│
├── docker-compose.yml           # Docker Compose configuration
├── multi_stage_build.Dockerfile # Multi-stage build file
└── env.sample                   # Sample environment variables
```

## 📊 Database Migrations

Migrations manage database schema changes. The database is typically updated automatically on startup, but you can manually manage migrations:

```bash
# Create new migrations from model changes
docker compose exec app python manage.py makemigrations

# Apply all pending migrations
docker compose exec app python manage.py migrate

# Show migration status
docker compose exec app python manage.py showmigrations

# Show migrations for a specific app
docker compose exec app python manage.py showmigrations booking
```

## 🔒 Security Considerations

### Critical Security Checklist

- [ ] **Environment Variables**: Never commit `.env` files with real credentials
  - Use `.env.example` or `env.sample` in version control
  - Store actual secrets in deployment secrets manager

- [ ] **Secret Key**: Generate a strong `SECRET_KEY` for production

  ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
  ```

- [ ] **Debug Mode**: Always disable `DEBUG=False` in production
  - Set `DEBUG=True` only in development
  - Exposing debug info can leak sensitive data

- [ ] **ALLOWED_HOSTS**: Configure appropriate hosts for production

    ```.dotenv
    ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
    ```

- [ ] **Database Security**
  - [ ] Change default PostgreSQL password
  - [ ] Use strong passwords (20+ characters)
  - [ ] Run database on private network in production
  - [ ] Regular backups

- [ ] **Admin Credentials**
  - [ ] Change default admin password immediately
  - [ ] Use strong passwords for superusers
  - [ ] Limit admin access to trusted IPs

- [ ] **Email Security**
  - [ ] Use proper TLS/SSL for production email servers
  - [ ] Never store sensitive data in email templates
  - [ ] Validate email addresses

- [ ] **HTTPS/SSL**
  - [ ] Use HTTPS in production
  - [ ] Configure SSL certificates
  - [ ] Set `SECURE_SSL_REDIRECT=True`

- [ ] **CORS & CSRF Protection**
  - [ ] Configure CORS headers properly
  - [ ] Keep CSRF protection enabled
  - [ ] Use Django's CSRF middleware

- [ ] **Data Protection**
  - [ ] Implement proper access controls
  - [ ] Validate all user inputs
  - [ ] Use Django ORM to prevent SQL injection
  - [ ] Sanitize output to prevent XSS

- [ ] **Dependencies**
  - [ ] Regularly update packages: `pip list --outdated`
  - [ ] Run security checks: `pip-audit`
  - [ ] Monitor for vulnerabilities

## 🐛 Troubleshooting

### Services Won't Start

**Check service status:**

```bash
docker compose ps
```

**Check for errors:**

```bash
docker compose logs
```

**Full restart:**

```bash
docker compose down -v
docker compose up -d --build
```

---

### Database Connection Issues

**Check if database is healthy:**

```bash
docker compose exec db pg_isready -U maktabiya
```

**View database logs:**

```bash
docker compose logs db
```

**Connect to database and check tables:**

```bash
docker compose exec db psql -U maktabiya -d maktabiya -c "\dt"
```

**Reset database (warning: loses all data):**

```bash
docker compose down -v
docker compose up -d
```

### Application Won't Start or Errors on Startup

**Check application logs:**

```bash
docker compose logs app
```

**Run migrations manually:**

```bash
docker compose exec app python manage.py migrate
```

**Check static files:**

```bash
docker compose exec app python manage.py collectstatic --noinput
```

**Create default admin user:**

```bash
docker compose exec app python manage.py createsuperuser
```

### Performance Issues

**Check resource usage:**

```bash
docker stats
```

**Scale task workers:**

```bash
docker compose up -d --scale tasks=3
```

**Monitor logs:**

```bash
docker compose logs -f
```

## 💻 Development Tips

### Code Style & Formatting

```bash
# Format code with Black
docker compose exec app black .

# Check code formatting
docker compose exec app black --check .
```

### Django Shell

Access Django shell for interactive development:

```bash
docker compose exec app python manage.py shell_plus

# Example queries:
# >>> from booking.models import Booking
# >>> from django.utils import timezone
# >>> Booking.objects.filter(booked_on__date=timezone.now()).count()
```

### Admin Panel Features

The admin (`/admin/`) provides:

- **Dashboard**: overview of booking and task status with live updates
- **Office Management**: Create and edit offices, rooms, and desks
- **Booking Administration**: View and manage all bookings
- **User Management**: Create users, assign managers, view profiles
- **Email Templates**: Manage booking confirmation and reminder emails
- **Task Monitoring**: View Django Q2 task queue status

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact & Support

For questions, issues, or suggestions:

- **Issue Tracker**: [GitHub Issues](https://github.com/Aladdin-97/pycon-talk-2026/issues)
- **Documentation**: See README file for detailed documentation

## 🙏 Acknowledgments

- Built with:
  - [Django](https://www.djangoproject.com/)
  - [Django Split Settings](https://django-split-settings.readthedocs.io/)
  - [Django Q2](https://django-q2.readthedocs.io/)
  - [PostgreSQL](https://www.postgresql.org/docs/)
- Admin interface powered by [Django Jazzmin](https://github.com/farridav/django-jazzmin)
- Email testing with [Mailpit](https://mailpit.io/)
- Containerized with [Docker](https://www.docker.com/)
