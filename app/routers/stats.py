from datetime import date, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise, MuscleGroup
from app.routers.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get all-time stats summary"""
    total_workouts = db.query(Workout).filter(Workout.user_id == current_user.id).count()

    total_exercises = db.query(Exercise).join(Workout).filter(
        Workout.user_id == current_user.id
    ).count()

    total_volume = db.query(func.sum(Exercise.sets * Exercise.reps)).join(Workout).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    return {
        "total_workouts": total_workouts,
        "total_exercises": total_exercises,
        "total_volume": total_volume
    }


@router.get("/weekly")
def get_weekly_stats(
    start_date: Optional[date] = Query(None, description="Start of week"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get stats for a specific week"""
    if not start_date:
        today = date.today()
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)

    end_date = start_date + timedelta(days=6)

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_date,
        Workout.date <= end_date
    ).all()

    workout_count = len(workouts)
    workout_ids = [w.id for w in workouts]

    exercises = db.query(Exercise).filter(Exercise.workout_id.in_(workout_ids)).all() if workout_ids else []

    muscle_groups = set(e.muscle_group.value for e in exercises)
    total_volume = sum(e.sets * e.reps for e in exercises)

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "workout_count": workout_count,
        "exercise_count": len(exercises),
        "muscle_groups_trained": len(muscle_groups),
        "total_volume": total_volume
    }


@router.get("/muscle-groups")
def get_muscle_group_stats(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """Get volume by muscle group for the last N days"""
    start_date = date.today() - timedelta(days=days)

    results = db.query(
        Exercise.muscle_group,
        func.sum(Exercise.sets * Exercise.reps).label("volume"),
        func.count(Exercise.id).label("exercise_count")
    ).join(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_date
    ).group_by(Exercise.muscle_group).all()

    return [
        {
            "muscle_group": r.muscle_group.value,
            "volume": r.volume or 0,
            "exercise_count": r.exercise_count
        }
        for r in results
    ]


@router.get("/streak")
def get_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get current workout streak"""
    workouts = db.query(Workout.date).filter(
        Workout.user_id == current_user.id
    ).order_by(Workout.date.desc()).all()

    if not workouts:
        return {"current_streak": 0, "longest_streak": 0}

    workout_dates = set(w.date for w in workouts)
    today = date.today()

    # Calculate current streak
    current_streak = 0
    check_date = today
    while check_date in workout_dates or (check_date == today and (today - timedelta(days=1)) in workout_dates):
        if check_date in workout_dates:
            current_streak += 1
        check_date -= timedelta(days=1)
        if check_date not in workout_dates and check_date != today:
            break

    # Calculate longest streak
    sorted_dates = sorted(workout_dates)
    longest_streak = 1
    current = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i] - sorted_dates[i-1]).days == 1:
            current += 1
            longest_streak = max(longest_streak, current)
        else:
            current = 1

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak if sorted_dates else 0
    }
