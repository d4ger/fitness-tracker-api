import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class MuscleGroup(str, enum.Enum):
    CHEST = "Chest"
    BACK = "Back"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    ARMS = "Arms"
    CORE = "Core"
    CARDIO = "Cardio"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=False)
    name = Column(String, nullable=False)
    muscle_group = Column(Enum(MuscleGroup), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=True)  # in kg or lbs
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workout = relationship("Workout", back_populates="exercises")
