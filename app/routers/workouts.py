"""
Workout tracking endpoints (all require a valid JWT):
  POST /workouts   - log a new exercise entry for the current user
  GET  /workouts   - retrieve the current user's full workout history
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User, WorkoutLog
from app.schemas import WorkoutLogCreate, WorkoutLogOut

router = APIRouter(prefix="/workouts", tags=["Workout Logging"])


@router.post("", response_model=WorkoutLogOut, status_code=status.HTTP_201_CREATED)
def log_workout(
    payload: WorkoutLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record a single exercise entry (sets/reps/weight) for the logged-in user."""
    log = WorkoutLog(
        exercise_name=payload.exercise_name,
        sets=payload.sets,
        reps=payload.reps,
        weight=payload.weight,
        user_id=current_user.id,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("", response_model=List[WorkoutLogOut])
def get_my_workout_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return every workout log tied to the current user, most recent first."""
    return (
        db.query(WorkoutLog)
        .filter(WorkoutLog.user_id == current_user.id)
        .order_by(WorkoutLog.logged_at.desc())
        .all()
    )
