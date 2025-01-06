from fastapi import APIRouter, Depends, HTTPException  # , status
from sqlalchemy.orm import Session
# from app import models, schemas, utils
from app.schemas import user as schemas
from app.models import user as models
from app.db.session import get_db
from app.controllers import auth as auth_controller
from app.utils.auth import create_access_token, verify_password, hash_password

router = APIRouter()


# User Registration
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create password hash
    hashed_password = hash_password(user.password)

    # Create new user
    db_user = models.User(
        username=user.username, password_hash=hashed_password, role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# User Login
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if not db_user or not verify_password(
        user.password, db_user.password_hash
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Get logged-in user's details
@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: schemas.UserResponse = Depends(auth_controller.get_current_user),
):
    return current_user


# Logout (invalidate JWT on client side)
@router.post("/logout")
def logout():
    # Log out by just deleting the token on the client side
    return {"message": "Logged out successfully"}
