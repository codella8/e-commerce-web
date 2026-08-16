# Karnoo — Django E-commerce Platform

A multilingual e-commerce platform built with Python and Django, featuring product management, shopping cart, checkout, order management, user profiles, and database integration.

## Overview

Karnoo is a server-rendered Django e-commerce application designed for online stores that need product management, customer accounts, shopping cart functionality, checkout workflows, and order management.

The project supports multiple languages and uses Persian as the default language.

The application is structured around three main areas:

- Storefront
- Shopping Cart
- Checkout & Orders

## Key Features

### Product Management

- Product catalog
- Product categories
- Product images
- Sale pricing
- Product validation
- Multilingual product fields

### Shopping Cart

- Session-based cart support
- Guest cart support
- Authenticated user cart support
- Cart items
- Quantity management

### Checkout & Orders

- Shipping information
- Checkout workflow
- Order creation
- Order items
- Order status management
- Order history

### User Accounts

- User authentication
- User profiles
- Address management
- Phone number
- Previous cart association

### Administration

- Django admin integration
- Product management
- Category management
- Order management
- User management

### Internationalization

Supported languages:

- Persian
- English
- Arabic
- Urdu

## Technology Stack

- Python
- Django
- PostgreSQL / SQLite
- django-modeltranslation
- Pillow
- django-jalali
- jdatetime
- HTML
- CSS

## Project Structure

text 
e-commerce-web/
├── app1/
├── cart/
├── payment/
├── karnoo/
├── locale/
├── mediafiles/
├── staticfiles/
├── manage.py
└── requirements.txt

## Application Architecture

### `app1`

Main storefront application responsible for:

- Products
- Categories
- User profiles
- Authentication
- Product pages
- Forms
- Translations

### `cart`

Shopping cart functionality responsible for:

- Cart management
- Cart items
- Session-based cart
- Cart utilities

### `payment`

Checkout and order management responsible for:

- Payment address
- Orders
- Order items
- Checkout workflow

### `karnoo`

Main Django project configuration containing:

- Settings
- URLs
- WSGI
- ASGI

## Installation

Clone the repository:

bash 
git clone https://github.com/codella8/e-commerce-web.git
cd e-commerce-web

Create a virtual environment:
python -m venv .venv

Activate it on Windows:
.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Create an administrator:
python manage.py createsuperuser

Collect static files:
python manage.py collectstatic --noinput

Run the development server:
python manage.py runserver

Open the application:
http://127.0.0.1:8000/

Configuration
Before production deployment, review the following settings:
SECRET_KEY
DEBUG
ALLOWED_HOSTS
Database configuration
Static files
Media files
Environment variables
For production, PostgreSQL is recommended instead of the development SQLite database.

Payment Integration
The current project includes checkout and order creation functionality.

An external payment gateway and provider webhook integration are not currently implemented.

Orders can be created and stored with their corresponding status.

## Screenshots

### Homepage

![Karnoo Homepage](docs/screenshots/homepage.png)

### Product Listing

![Karnoo Product Listing](docs/screenshots/product.png)

### Product Detail

![Karnoo Product Detail](docs/screenshots/product-detail.png)

### Shopping Cart

![Karnoo Shopping Cart](docs/screenshots/cart.png)

### Checkout

![Karnoo Checkout](docs/screenshots/contact.png)

### About
![Karnoo Checkout](docs/screenshots/about.png)

### Login
![Karnoo Checkout](docs/screenshots/login.png)

### Admin Dashboard

![Karnoo Admin Dashboard](docs/screenshots/admin-dashboard.png)

Active development / portfolio project.
Future Improvements
Potential improvements include:

Payment gateway integration
Automated email notifications
Expanded test coverage
CI workflow
Production deployment configuration
Redis caching
Additional security hardening
REST API integration

Author
Shamsia Mohammadi

Python Django Backend Developer

GitHub: https://github.com/codella8
Portfolio: https://azingroup.com
License

See the repository license for usage and distribution information.
















