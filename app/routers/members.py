from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, security

# 1. Initialize the router with a web prefix and category tags
router = APIRouter(
    prefix="/members",
    tags=["Members & Authentication"]
)

# 2. Database Session Connection Provider
def get_db():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 1. ROUTE: USER REGISTRATION (/members/register)
# ==========================================
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if a user with this email address already exists
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address is already registered."
        )
    
    # Hash the plain-text password securely before it touches the disk
    hashed_pass = security.hash_password(user_in.password)
    
    # Create the SQLAlchemy instance mapping to the users table layout
    new_user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_pass,
        role=user_in.role
    )
    
    # Stage, save, and refresh our database record
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
