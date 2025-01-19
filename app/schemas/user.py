from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    password: str  # For user registration, password is required


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True  # To serialize SQLAlchemy models to Pydantic models


class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
