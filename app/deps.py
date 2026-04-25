"""
Shared dependencies used across routers via FastAPI's `Depends`.

get_current_user reads the bearer token from the Authorization header,
decodes it, and loads the matching user from the database - this is
what "protects" an endpoint (just add `Depends(get_current_user)`).
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

# tokenUrl points at the login endpoint, used only for interactive
# /docs "Authorize" button - actual verification happens below.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def require_staff(current_user: User = Depends(get_current_user)) -> User:
    """
    Gate for endpoints that only trainers/admins should perform, such as
    creating a class schedule. Regular members are rejected with 403.
    """
    if current_user.role not in ("trainer", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only trainers or admins can perform this action.",
        )
    return current_user
