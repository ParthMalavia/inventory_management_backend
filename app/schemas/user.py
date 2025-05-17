from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.utils.enums import UserRole


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    role: UserRole = UserRole.staff


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    password: str  # For user registration, password is required


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # To serialize SQLAlchemy models to Pydantic models


class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
