from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# 1. Setup Password Hashing Context
# Tells passlib to use the bcrypt algorithm under the hood
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    

# 2. JWT Configuration Variables
# Security Notice: Keep this secret key completely private in production!
SECRET_KEY = "SUPER_SECRET_FLEETFIT_KEY_THAT_NO_ONE_SHOULD_KNOW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password : str ) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Utility: Generate a secure signed JWT access token
def create_access_token(data : dict) -> str:
    to_encode = data.copy()

    # Calculate the exact timestamp when this token should expire (1 hour from now)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode.update({"exp": expire})

    # Cryptographically sign the token payload with our secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt
