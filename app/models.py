from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True ,nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True,nullable=False)
    role = Column(String, index=True, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    workouts = relationship("WorkoutLog", back_populates="user")
    trained_classes = relationship("ClassSchedule", back_populates="user")


class WorkoutLog(Base):
    __tablename__ = "Workout_logs"   

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete = "CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)
    muscle_group = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="workouts")

class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False)     # e.g., "HIIT Circuit"
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)  
    current_enrolled = Column(Integer, default=0)

    trainer = relationship("User", back_populates="trained_classes")    