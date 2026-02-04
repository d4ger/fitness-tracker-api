from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.exercise import ExerciseResponse, ExerciseCreate


class WorkoutBase(BaseModel):
    date: date
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    exercises: Optional[List[ExerciseCreate]] = []


class WorkoutUpdate(BaseModel):
    date: Optional[date] = None
    notes: Optional[str] = None


class WorkoutResponse(WorkoutBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    exercises: List[ExerciseResponse] = []

    class Config:
        from_attributes = True
