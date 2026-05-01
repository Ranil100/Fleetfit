"""
Fitness class scheduling endpoints:
  POST /classes   - (trainer/admin only) publish a new class
  GET  /classes   - browse all scheduled classes, with live open-spot counts
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.deps import require_staff
from app.models import FitnessClass, Booking, User
from app.schemas import FitnessClassCreate, FitnessClassOut

router = APIRouter(prefix="/classes", tags=["Fitness Classes"])


@router.post("", response_model=FitnessClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    payload: FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    """Publish a new fitness class (trainers/admins only)."""
    new_class = FitnessClass(
        title=payload.title,
        trainer_name=payload.trainer_name,
        start_time=payload.start_time,
        capacity=payload.capacity,
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    result = FitnessClassOut.model_validate(new_class)
    result.spots_remaining = new_class.capacity
    return result


@router.get("", response_model=List[FitnessClassOut])
def list_classes(db: Session = Depends(get_db)):
    """
    Browse every scheduled class. Each entry includes spots_remaining,
    computed live from the booking count, so clients can see availability
    without a separate request.
    """
    classes = db.query(FitnessClass).order_by(FitnessClass.start_time).all()

    booking_counts = dict(
        db.query(Booking.class_id, func.count(Booking.id))
        .group_by(Booking.class_id)
        .all()
    )

    output = []
    for cls in classes:
        item = FitnessClassOut.model_validate(cls)
        booked = booking_counts.get(cls.id, 0)
        item.spots_remaining = max(cls.capacity - booked, 0)
        output.append(item)

    return output
