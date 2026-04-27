"""
Pydantic schemas: validate incoming request bodies and shape outgoing
JSON responses. `from_attributes = True` lets a schema read directly
off SQLAlchemy ORM objects (so we never hand-write dict conversions),
and fields like hashed_password are simply omitted from response
schemas so they're never leaked to the client.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models import UserRole


# ---------- Users ----------

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: UserRole = UserRole.member


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Workout Logs ----------

class WorkoutLogCreate(BaseModel):
    exercise_name: str = Field(..., min_length=1, max_length=100)
    sets: int = Field(..., gt=0, le=100)
    reps: int = Field(..., gt=0, le=1000)
    weight: float = Field(..., ge=0, le=1000)


class WorkoutLogOut(BaseModel):
    id: int
    exercise_name: str
    sets: int
    reps: int
    weight: float
    logged_at: datetime

    class Config:
        from_attributes = True


# ---------- Fitness Classes ----------

class FitnessClassCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    trainer_name: str = Field(..., min_length=1, max_length=100)
    start_time: datetime
    capacity: int = Field(..., gt=0, le=1000)


class FitnessClassOut(BaseModel):
    id: int
    title: str
    trainer_name: str
    start_time: datetime
    capacity: int
    spots_remaining: Optional[int] = None

    class Config:
        from_attributes = True


# ---------- Bookings ----------

class BookingCreate(BaseModel):
    class_id: int


class BookingOut(BaseModel):
    id: int
    class_id: int
    user_id: int
    booked_at: datetime

    class Config:
        from_attributes = True
