# Secure Password Manager (USC_TIA Compliant)

## Overview
A secure, Python-based password manager that stores credentials in a PostgreSQL database using Fernet encryption. This project complies with USC_TIA standards by handling sensitive keys via environment variables.

## Features
* **Secure Storage:** AES-128 (Fernet) encryption for all passwords.
* **Zero-Knowledge Key Loading:** The master key is loaded from the system environment, never hardcoded.
* **CRUD Operations:** Create, Read, Update, and Delete passwords.
* **Strong Password Generator:** Built-in tool to create cryptographically strong credentials.

## Installation & Setup

### 1. Prerequisites
* Python 3.10+
* PostgreSQL Database

### 2. Environment Configuration (CRITICAL)
For security compliance, you must set up the `.env` file before running the application.

1.  Create a file named `.env` in the root directory.
2.  Add the following variables:
    ```ini
    DB_NAME=pass_manager
    DB_USER=postgres
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    MASTER_ENCRYPTION_KEY=Your_Base64_Key_Here
    ```

### 3. How to Run
To run the application from the source:
```bash
python main.py