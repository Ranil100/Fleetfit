from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ==========================================
# 1. USER SCHEMAS (Handling Data Shapes)
# ==========================================

# Base properties shared across both incoming inputs and outgoing outputs
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[str] = "member"  # Defaults to "member" if not specified

# Input Schema: What a user client sends when registering an account
class UserCreate(UserBase):
    password: str  # Plain text password from user registration input

# Output Schema: The clean data safe to send back to the client/browser
class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Configures Pydantic to read database model objects natively
    class Config:
        from_attributes = True


# ==========================================
# 2. AUTHENTICATION SCHEMAS (Handling JWT Tokens)
# ==========================================

# Shape of the JSON response payload returned upon successful login
class Token(BaseModel):
    access_token: str
    token_type: str

# Shape of the data extracted and decoded from inside a verified token payload
class TokenData(BaseModel):
    user_id: Optional[int] = None
