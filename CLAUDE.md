# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for the Fitness Tracker mobile app. Provides REST API for user authentication, workout tracking, and statistics.

## Development Commands

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Run development server
uvicorn app.main:app --reload

# Run with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Architecture

### Project Structure

```
app/
├── main.py           # FastAPI app entry point
├── core/
│   ├── config.py     # Settings from environment
│   └── security.py   # JWT and password utilities
├── db/
│   └── database.py   # SQLAlchemy engine and session
├── models/           # SQLAlchemy ORM models
│   ├── user.py
│   ├── workout.py
│   └── exercise.py
├── schemas/          # Pydantic request/response schemas
│   ├── user.py
│   ├── workout.py
│   └── exercise.py
└── routers/          # API endpoints
    ├── auth.py       # /api/auth/*
    ├── workouts.py   # /api/workouts/*
    ├── exercises.py  # /api/workouts/{id}/exercises/*
    └── stats.py      # /api/stats/*
```

### Key Patterns

- **UUID primary keys** for all models
- **JWT authentication** via OAuth2 Bearer token
- **Nested routes** for exercises under workouts
- **Pydantic schemas** separate from SQLAlchemy models
- **Dependency injection** for database sessions and current user

### Authentication Flow

1. Register: `POST /api/auth/register`
2. Login: `POST /api/auth/login` (returns JWT)
3. Use token: `Authorization: Bearer <token>`
4. Get user: `GET /api/auth/me`

### Database

PostgreSQL with SQLAlchemy ORM. Tables created automatically on startup via `Base.metadata.create_all()`.

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
