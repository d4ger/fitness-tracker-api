# Fitness Tracker API

Backend API for the Fitness Tracker mobile app built with FastAPI and PostgreSQL.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Validation:** Pydantic

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user

### Workouts
- `GET /api/workouts` - List workouts (with date filters)
- `GET /api/workouts/week` - Get current week's workouts
- `GET /api/workouts/date/{date}` - Get workout by date
- `GET /api/workouts/{id}` - Get workout by ID
- `POST /api/workouts` - Create workout
- `PUT /api/workouts/{id}` - Update workout
- `DELETE /api/workouts/{id}` - Delete workout

### Exercises
- `GET /api/workouts/{workout_id}/exercises` - List exercises
- `POST /api/workouts/{workout_id}/exercises` - Add exercise
- `PUT /api/workouts/{workout_id}/exercises/{id}` - Update exercise
- `DELETE /api/workouts/{workout_id}/exercises/{id}` - Delete exercise

### Statistics
- `GET /api/stats/summary` - All-time stats
- `GET /api/stats/weekly` - Weekly stats
- `GET /api/stats/muscle-groups` - Volume by muscle group
- `GET /api/stats/streak` - Workout streak

## Database Schema

```
users
├── id (UUID)
├── email
├── username
├── hashed_password
├── full_name
├── created_at
└── updated_at

workouts
├── id (UUID)
├── user_id (FK)
├── date
├── notes
├── created_at
└── updated_at

exercises
├── id (UUID)
├── workout_id (FK)
├── name
├── muscle_group (enum)
├── sets
├── reps
├── weight
├── notes
└── created_at
```
