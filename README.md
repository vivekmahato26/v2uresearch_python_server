# V2U Research App

**V2U Research App** is a robust Django-based web application designed to deliver financial research, market insights, and company intelligence. It features a multi-regional architecture, dynamic content management, and a secure user platform.

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Core Features](#core-features)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Database & Schema](#database--schema)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

V2U Research provides users with access to:

- **Daily Research Reports**: In-depth analysis of markets and companies.
- **Sector Intelligence**: Aggregated data across various industries (Technology, Healthcare, Mining, etc.).
- **Product Store**: Access to specialized trading products and report packages.
- **Regional Customization**: Localized content for Australia (AUS), Canada (CAN), and USA.

---

## Technology Stack

### Backend

- **Framework**: Django 5.0+ (Python 3.10+)
- **Database**: MySQL (via `pymysql` driver)
- **API**: Django Rest Framework (DRF)
- **Authentication**: `django-allauth` for secure functionality.

### Frontend

- **Templating**: Django Templates (DTL)
- **Styling**: Bootstrap 5, Custom CSS
- **Interactivity**: Vanilla JavaScript, FontAwesome Icons

### Utilities & Services

- **Storage**: AWS S3 (`boto3`, `django-storages`) for static and media assets.
- **Rich Text**: `django-ckeditor` for content management.
- **Exports**: `django-csv-export-view` for data reporting.

---

## Project Architecture

The project is modularized into several Django apps, each handling specific domains:

### Core Apps

| App Name        | Description                                                                                                     |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- |
| **`home`**      | Manages the Landing Page, static pages (About/Contact), and global mixins (`EssentialsMixin`) for context data. |
| **`users`**     | Handles User models (`User`), Authentication, and `Region` management.                                          |
| **`reports`**   | Core engine for Research Reports, Daily Updates, and content publishing.                                        |
| **`company`**   | manages `Company` profiles and `Sector` categorizations.                                                        |
| **`marketing`** | Handles `Products`, `Leads`, and subscriptions/packages.                                                        |

### Support Apps

| App Name           | Description                                                       |
| :----------------- | :---------------------------------------------------------------- |
| **`testimonials`** | Manages client feedback (with custom carousel UI).                |
| **`feeder`**       | Data ingestion pipelines (for importing external financial data). |
| **`sales`**        | Sales management and tracking.                                    |
| **`apis`**         | REST API endpoints for external integrations.                     |

---

## Core Features

### 1. Dynamic Region Management

- **Multi-Region Support**: The site content adapts based on the user's selected region (AUS, CAN, USA).
- **Selection Mechanism**: A header dropdown allows users to switch regions. The choice is persisted via cookies.
- **Active Filtering**: Only `Active` regions (configurable in Admin) are visible to users.

### 2. Research Hub

- **Public & Private Access**: General research is public (`/research/`), while specialized dashboards (`/dashboard-report/`) are protected.
- **Advanced Filtering**: Users can filter reports by Sector, Date, or Research Type.

### 3. Sector Intelligence

- **Priority Ordering**: Sectors are displayed based on a custom `Priority` score.
- **Dedicated View**: A "View All Sectors" page allows users to explore industries visually.

### 4. Modern UI/UX

- **Responsive Design**: Fully mobile-optimized layouts using Bootstrap & Flexbox.
- **Custom Components**: Includes bespoke carousels for testimonials and interactive "View All" navigation elements.

---

## Installation & Setup

### 1. Prerequisites

- Python 3.10+
- MySQL Server running locally or remotely.

### 2. Setup Steps

1.  **Clone/Navigate to Project**:

    ```bash
    cd /home/cs/Desktop/v2uresearch/v2ur_backup/V2UResearchApp
    ```

2.  **Environment Setup**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    _Note: `pymysql` is used as a drop-in replacement for `mysqlclient`._

4.  **Database Configuration**:
    Edit `V2UResearchApp/settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'v2uresearch',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    ```

5.  **Initialize Database**:
    ```bash
    python manage.py migrate
    ```

---

## Running the Application

Start the development server:

```bash
python manage.py runserver
```

- **Local Address**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## Database & Schema

### Important Models

- **`User` (users)**: Custom user model extending standard authentication.
- **`Region` (users)**: Controls site localization. Key fields: `country_code`, `is_active`, `is_default`.
- **`Sector` (company)**: Industry categories. Key field: `priority` (for display ordering).
- **`Report` (reports)**: The central content unit. Linked to Regions, Sectors, and Products.

### Recent Schema Updates

- **Sector.priority**: Added `IntegerField` to control display order on Homepage.
- **Region.is_active**: Strict filtering enforced to only show supported regions (AUS, CAN, USA).

---

## Troubleshooting

### Templating Issues

- **`Property assignment expected`**: Occurs if Django template tags are unquoted in JS objects.
  - _Fix_: Wrap in quotes: `'{{ value }}'`.

### Region Dropdown Clutter

- If the header shows too many countries, run this Django shell command to cleanup:
  ```python
  from users.models import Region
  Region.objects.exclude(country_code__in=['AUS', 'CAN', 'USA']).update(is_active=False)
  ```

### Static Files

- The logo is served locally from `static/images/Logo.svg`. Ensure this file exists when deploying.
# v2uresearch_python_server
# v2uresearch_python_server
