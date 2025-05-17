from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.category import Category


# Base schema for common fields
class InventoryBase(BaseModel):
    part_number: str
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    low_stock_threshold: Optional[int] = 10
    category_id: int  # Required field linking to category


# Schema for creating a new item
class InventoryCreate(InventoryBase):
    pass


# Schema for updating an item (all fields optional)
class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    low_stock_threshold: Optional[int] = None
    category_id: Optional[int] = None


# Schema for quantity-specific updates
class InventoryQuantityUpdate(BaseModel):
    quantity: int


# Schema for response (includes DB fields like ID and timestamps)
class Inventory(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = (
        None  # Optional: Include category details in response
    )

    class Config:
        from_attributes = True
