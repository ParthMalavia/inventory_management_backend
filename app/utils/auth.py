from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt

import bcrypt
from fastapi.security import OAuth2PasswordBearer
from app.models import user as models
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as schemas

# from app.models.user import User
from app.config import settings

# OAuth2 token handler
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# JWT Secret Key and algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Hash a password
def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


# Verify a password
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password)


# Create JWT token
def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def user_login(user: schemas.UserLogin, db: Session):
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
