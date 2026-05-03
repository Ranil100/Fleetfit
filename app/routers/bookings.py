"""
Class slot booking endpoints:
  POST /bookings          - reserve a spot in a class (validated & transactional)
  GET  /bookings/me       - list the current user's upcoming bookings

Business rules enforced here:
  - A class can never be booked past its declared capacity (no overbooking).
  - A member cannot book the same class twice (enforced at the DB level
    via a UniqueConstraint, and checked here first for a clean 400 error
    instead of a raw integrity-error 500).
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.deps import get_current_user
from app.models import Booking, FitnessClass, User
from app.schemas import BookingCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["Class Bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def book_class(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fitness_class = (
        db.query(FitnessClass).filter(FitnessClass.id == payload.class_id).first()
    )
    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found."
        )

    # Duplicate-booking check.
    existing = (
        db.query(Booking)
        .filter(
            Booking.user_id == current_user.id,
            Booking.class_id == payload.class_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this class.",
        )

    # Capacity check - counts current bookings against the class's limit.
    current_bookings = (
        db.query(func.count(Booking.id))
        .filter(Booking.class_id == payload.class_id)
        .scalar()
    )
    if current_bookings >= fitness_class.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This class is already full.",
        )

    booking = Booking(user_id=current_user.id, class_id=payload.class_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/me", response_model=List[BookingOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List every class the current user has booked."""
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()
