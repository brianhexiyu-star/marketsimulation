# Market Simulation

A full-stack Flask marketplace application built with Python, SQLAlchemy, Flask-WTF, and a Jinja-based web interface.

The project explores user accounts, authentication, marketplace logic, database persistence, and deployment-oriented configuration.

## Features

- User authentication and account management
- Marketplace functionality
- Market-item data models
- Premium functionality
- CSRF protection
- SQLAlchemy database integration
- Flask application factory
- SQLite for local development
- PostgreSQL through DATABASE_URL
- Vercel-oriented deployment configuration

## Tech Stack

### Backend

- Python
- Flask 3
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF
- SQLAlchemy
- Gunicorn

### Database

- SQLite for local development
- PostgreSQL for deployment

### Frontend

Jinja templates served by Flask.

## Structure

~~~text
.
├── main.py
├── requirements.txt
├── vercel.json
└── website/
    ├── init.py
    ├── auth.py
    ├── account.py
    ├── market.py
    ├── model.py
    ├── premium.py
    ├── views.py
    └── templates/
~~~

## Running Locally

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
~~~

The application can fall back to SQLite locally. For deployment, provide DATABASE_URL for PostgreSQL.

## Configuration

Environment-based configuration includes SECRET_KEY, DATABASE_URL, and SESSION_COOKIE_SECURE. Keep real credentials and production secrets outside the repository.

## Learning Goals

The project was built as a practical step toward backend and full-stack development, with emphasis on authentication, relational databases, forms, CSRF protection, modular Flask architecture, and deployment.

## Status

Learning and portfolio project.