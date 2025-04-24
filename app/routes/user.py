from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.models import user as user_model
from app.db.session import get_db
from app.controllers.auth import get_current_user

router = APIRouter()


# Get all users
@router.get("/users", response_model=list[user_schema.UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    users = db.query(user_model.User).all()
    return users


# Get user by ID
@router.get("/users/{user_id}", response_model=user_schema.UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user by ID
@router.put("/users/{user_id}", response_model=user_schema.UserResponse)
async def update_user(
    user_id: int,
    user: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user is authorized to update this user
    if db_user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to update this user"
        )

    user_data = user.dict(exclude_unset=True)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Delete user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this user"
        )
    db.delete(db_user)
    db.commit()
