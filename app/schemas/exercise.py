from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel


class MuscleGroup(str, Enum):
    CHEST = "Chest"
    BACK = "Back"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    ARMS = "Arms"
    CORE = "Core"
    CARDIO = "Cardio"


class ExerciseBase(BaseModel):
    name: str
    muscle_group: MuscleGroup
    sets: int
    reps: int
    weight: Optional[int] = None
    notes: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    muscle_group: Optional[MuscleGroup] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None
    notes: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    id: UUID
    workout_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
