"""
ORM models. These map directly to database tables and are auto-created
on startup via Base.metadata.create_all() in main.py.
"""
import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    member = "member"
    trainer = "trainer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.member, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One-to-many: a user has many workout logs and many bookings.
    workout_logs = relationship(
        "WorkoutLog", back_populates="owner", cascade="all, delete-orphan"
    )
    bookings = relationship(
        "Booking", back_populates="member", cascade="all, delete-orphan"
    )


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)  # in kg
    logged_at = Column(DateTime, default=datetime.utcnow)

    # Foreign key back to the owning user.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="workout_logs")


class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    trainer_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)

    bookings = relationship(
        "Booking", back_populates="fitness_class", cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"
    # A member can only book a given class once (prevents duplicate booking).
    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uq_user_class_booking"),
    )

    id = Column(Integer, primary_key=True, index=True)
    booked_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False)

    member = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")
