# StudyFlow

StudyFlow is a Django-based web application that helps users learn and track their progress in different courses. It provides a clean, responsive interface and stores all progress securely in a database.

## Features

* User registration and login with password hashing
* Course progress tracking stored in the database
* Session-based authentication
* Simple, responsive UI built with HTML, CSS, and JavaScript
* SQLite backend for easy setup

## Project Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/rahuls465/StudyFlow.git
   cd StudyFlow
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:

   ```bash
   pip install django
   ```
4. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:

   ```bash
   python manage.py runserver
   ```
6. Open your browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Folder Structure

```
StudyFlow/
├── StudyFlow/         # Project settings
├── firstpage/         # App containing all views, models, templates
├── db.sqlite3         # Local database
├── manage.py
└── README.md
```

## API Endpoints

| Endpoint              | Method | Description                |
| --------------------- | ------ | -------------------------- |
| `/api/register/`      | POST   | Register a new user        |
| `/api/login/`         | POST   | Log in a user              |
| `/api/logout/`        | POST   | Log out current session    |
| `/api/session/`       | GET    | Check if user is logged in |
| `/api/progress/save/` | POST   | Save user progress         |
| `/api/progress/get/`  | GET    | Get user progress          |

## Author

**Rahul Mala**
