# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for the Fitness Tracker mobile app. Provides REST API for user authentication, workout tracking, and statistics.

**Tech Stack:** FastAPI, PostgreSQL, SQLAlchemy, JWT (python-jose), Pydantic

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
```

## Environment Variables

Required in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/fitness_tracker
SECRET_KEY=your-secret-key
ALGORITHM=HS256  # optional, defaults to HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60  # optional, defaults to 60
```

## Architecture

### Key Patterns

**Dependency Injection:** The `get_current_user` dependency in `app/routers/auth.py:19` validates JWT tokens and returns the authenticated User. Import and use it as a dependency in protected routes:
```python
from app.routers.auth import get_current_user
current_user: User = Depends(get_current_user)
```

**Database Sessions:** Use `get_db` from `app/db/database.py` for SQLAlchemy sessions. Tables are auto-created on startup via `Base.metadata.create_all()`.

**UUID Primary Keys:** All models use UUID primary keys via `UUID(as_uuid=True)`.

**One Workout Per Day:** Workouts are unique per user per date. Creating a workout for an existing date returns 400.

### MuscleGroup Enum

Defined in `app/models/exercise.py`:
- Chest, Back, Legs, Shoulders, Arms, Core, Cardio

### API Routes

All routes prefixed with `/api`:
- `/auth` - Authentication (login returns JWT in `access_token` field)
- `/workouts` - CRUD + `/week` (weekly view) + `/date/{date}` (lookup by date)
- `/workouts/{id}/exercises` - Nested exercise management
- `/stats` - Summary, weekly stats, muscle group breakdown, streak calculation

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
