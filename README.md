# B2B Credit Transaction Management System

The B2B Credit Transaction Management System is designed to manage the credit of sellers, facilitating charge sales to
phone numbers while ensuring accurate and atomic credit operations. This system ensures accounting consistency,
preventing negative balances and race conditions under heavy loads. The project includes user role management,
transaction logging, and secure API access, with a focus on high scalability and parallel load management.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Deployment](#deployment)
- [Switching Between Environments](#switching-between-environments)
- [Future Improvements](#future-improvements)

## Features

- User Role Management:
    - Supports roles like Admin and Seller.
    - Admins can manage deposit requests and user roles.
    - Sellers can request deposits and perform transfers.

- Deposit System:
    - Sellers can submit requests for deposits.
    - Admins can approve or deny deposit requests.
    - Automated logging of all deposits.

- Transaction Management:
    - Tracks various transactions including deposits and charge transfers to phone numbers.
    - Ensures all transactions are atomic and consistent.
    - Logs transaction details, including user, type, amount, and resulting balance.

- Signal-Driven Actions:
    - Implemented signals to trigger actions after certain events, like updating user balance after deposit
      approvals.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.10+** installed on your machine.
- **Virtualenv** or another method for managing virtual environments.
- **Docker** and **Docker Compose**.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Fsnk2001/credit-transaction-management
cd credit-transaction-management
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

- For development:
    ```bash
    pip install -r requirements.txt
    ```

- For production:
    ```bash
    pip install -r requirements-production.txt
    ```

## Environment Variables

Create a `.env` file in the project root directory and add the required environment.
You can copy the `.env.example` file:

```bash
cp .env.example .env
```

To generate a unique `SECRET_KEY` and set it in your `.env` file, use the provided script.

```bash
python generate_secret_key.py
```

This script will:

- Copy the `.env.example` file to `.env` if `.env` does not already exist.
- Generate a unique `SECRET_KEY` and add it to the `.env` file, ensuring you have a secure key for your application.

## Database Migrations

Apply the migrations to set up your database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

To deploy the project using Docker Compose, run this:

- For development:
    ```bash
    docker compose up --build -d
    ```

- For production:
    ```bash
    docker compose -f docker-compose-production.yml up --build -d
    ```

## Switching Between Environments

To switch between development and production settings, modify the environment variable `DJANGO_SETTINGS_MODULE` when
running the application.

- For development:
    ```bash
    export DJANGO_SETTINGS_MODULE=credit_transaction.settings.local
    ```

- For production:
    ```bash
    export DJANGO_SETTINGS_MODULE=credit_transaction.settings.production
    ```

## Future Improvements

- Role-Based Access Control (RBAC): Extend the permission system to support more granular roles and access levels.
- Transaction History API: Allow users to query their transaction history with filters (e.g., date, transaction type).
- Notifications: Implement real-time notifications for sellers when their credit request is approved.
