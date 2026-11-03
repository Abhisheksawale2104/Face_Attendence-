# Face Attendance

A Python desktop app for registering people, recording attendance with face
recognition, and reviewing attendance records. The project is being built in
small, testable steps.

## Current status

The initial setup, environment-based MySQL configuration, database
initialization, and desktop shell are in place. Face recognition and attendance
workflows will be added in later steps.

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

## Initialize the database

After setting the MySQL environment variables, create the database and tables:

```powershell
python initialize_database.py
```

The database user needs permission to create the configured database and its
tables. Initialization is safe to rerun; it creates missing tables without
deleting existing records.

## Run

```powershell
python main.py
```

## Development milestones

1. Establish project setup and safe local configuration.
2. Add configurable MySQL access and idempotent database initialization.
3. Build the desktop application shell and database status check.
4. Add person registration, face matching, attendance records, and reports.
