from datetime import date, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("", response_model=List[WorkoutResponse])
def get_workouts(
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Workout).filter(Workout.user_id == current_user.id)

    if start_date:
        query = query.filter(Workout.date >= start_date)
    if end_date:
        query = query.filter(Workout.date <= end_date)

    return query.order_by(Workout.date.desc()).all()


@router.get("/week", response_model=List[WorkoutResponse])
def get_week_workouts(
    start_date: Optional[date] = Query(None, description="Start of week (defaults to current week's Monday)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not start_date:
        today = date.today()
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)

    end_date = start_date + timedelta(days=6)

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_date,
        Workout.date <= end_date
    ).order_by(Workout.date).all()

    return workouts


@router.get("/date/{workout_date}", response_model=Optional[WorkoutResponse])
def get_workout_by_date(
    workout_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.date == workout_date
    ).first()
    return workout


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.post("", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout_data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if workout already exists for this date
    existing = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.date == workout_data.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workout already exists for this date. Use PUT to update."
        )

    workout = Workout(
        user_id=current_user.id,
        date=workout_data.date,
        notes=workout_data.notes
    )
    db.add(workout)
    db.flush()

    # Add exercises if provided
    for exercise_data in workout_data.exercises:
        exercise = Exercise(
            workout_id=workout.id,
            name=exercise_data.name,
            muscle_group=exercise_data.muscle_group,
            sets=exercise_data.sets,
            reps=exercise_data.reps,
            weight=exercise_data.weight,
            notes=exercise_data.notes
        )
        db.add(exercise)

    db.commit()
    db.refresh(workout)
    return workout


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: UUID,
    workout_data: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout_data.date is not None:
        workout.date = workout_data.date
    if workout_data.notes is not None:
        workout.notes = workout_data.notes

    db.commit()
    db.refresh(workout)
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()
