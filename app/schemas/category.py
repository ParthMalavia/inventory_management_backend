from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# from app.schemas.inventory import Inventory  # Import for relationship


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # items: Optional[List[Inventory]] = None

    class Config:
        from_attributes = True
