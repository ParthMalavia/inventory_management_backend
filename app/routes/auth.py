from fastapi import APIRouter, Depends, HTTPException  # , status
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.models import user as user_model
from app.db.session import get_db
from app.controllers import auth as auth_controller
from app.utils.auth import hash_password, user_login
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# User Registration
@router.post("/register", response_model=user_schema.UserResponse)
async def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = (
        db.query(user_model.User).filter(user_model.User.username == user.username).first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create password hash
    hashed_password = hash_password(user.password)

    # Create new user
    db_user = user_model.User(
        username=user.username, password_hash=hashed_password, role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Generate JWT token
@router.post("/token")
async def token(
        formdata: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
    user = user_schema.UserLogin(username=formdata.username, password=formdata.password)
    return user_login(user, db)


# User Login
@router.post("/login")
async def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    return user_login(user, db)


# Get logged-in user's details
@router.get("/me", response_model=user_schema.UserResponse)
async def get_me(
    current_user = Depends(auth_controller.get_current_user),
):
    return current_user


# Logout (invalidate JWT on client side)
@router.post("/logout")
async def logout():
    # Log out by just deleting the token on the client side
    return {"message": "Logged out successfully"}
