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

# ==========================================
# 2. ROUTE: USER LOGIN & JWT ISSUANCE (/members/login)
# ==========================================
@router.post("/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Look up the user profile by their email address
    # OAuth2PasswordRequestForm maps the email input field to 'form_data.username'
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. If user doesn't exist, or password check fails, return an unauthenticated block error
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate a secure cryptographic signed JWT token packet containing the user ID
    access_token = security.create_access_token(data={"user_id": user.id})
    
    # 4. Return the token according to the structural schema shape expected by Pydantic
    return {"access_token": access_token, "token_type": "bearer"}

