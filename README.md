# Face Attendance

A Python desktop app for registering people, recording attendance with face
recognition, and reviewing attendance records. The project is being built in
small, testable steps.

## Current status

The first development step lays the groundwork: project setup, safe local
configuration, and a desktop shell. Database setup and face recognition will
be added in subsequent steps.

## Requirements

- Python 3.10 or newer
- MySQL Server
- A webcam for the face-recognition stage

## Setup

From the project directory, create and activate a virtual environment, then
install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the MySQL connection settings in the current PowerShell session. For
example:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "your-local-mysql-password"
$env:MYSQL_DATABASE = "attendance"
```

Do not commit passwords or other secrets. `.env.example` documents the
supported settings; the application reads environment variables directly and
does not load `.env` files.

## Run

```powershell
python main.py
```

## Development milestones

1. Establish project setup and configuration.
2. Add a reusable MySQL connection and database initialization.
3. Build the desktop application shell and database status check.
4. Add person registration, face matching, attendance records, and reports.
