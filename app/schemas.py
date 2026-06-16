from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

# ==========================================
# 1. USER SCHEMAS (Handling Data Shapes)
# ==========================================

class UserBase(BaseModel):
    email:str
    full_name:str
    role:Optional[str] = "member"  # Default role is "member"

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# 2. AUTHENTICATION SCHEMAS (Handling JWT Tokens)
# ==========================================

class Token(BaseModel):
    access_token : str
    token_type : str

    
class TokenData(BaseModel):
    user_id : Optional[str] = None
