from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/workouts/{workout_id}/exercises", tags=["Exercises"])


def get_workout_or_404(workout_id: UUID, user_id: UUID, db: Session) -> Workout:
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user_id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.get("", response_model=List[ExerciseResponse])
def get_exercises(
    workout_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = get_workout_or_404(workout_id, current_user.id, db)
    return workout.exercises


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(
    workout_id: UUID,
    exercise_data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = get_workout_or_404(workout_id, current_user.id, db)

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
    db.refresh(exercise)
    return exercise


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    workout_id: UUID,
    exercise_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = get_workout_or_404(workout_id, current_user.id, db)

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.workout_id == workout.id
    ).first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    workout_id: UUID,
    exercise_id: UUID,
    exercise_data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = get_workout_or_404(workout_id, current_user.id, db)

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.workout_id == workout.id
    ).first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    if exercise_data.name is not None:
        exercise.name = exercise_data.name
    if exercise_data.muscle_group is not None:
        exercise.muscle_group = exercise_data.muscle_group
    if exercise_data.sets is not None:
        exercise.sets = exercise_data.sets
    if exercise_data.reps is not None:
        exercise.reps = exercise_data.reps
    if exercise_data.weight is not None:
        exercise.weight = exercise_data.weight
    if exercise_data.notes is not None:
        exercise.notes = exercise_data.notes

    db.commit()
    db.refresh(exercise)
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(
    workout_id: UUID,
    exercise_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = get_workout_or_404(workout_id, current_user.id, db)

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.workout_id == workout.id
    ).first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()
