from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.utils.enums import OrderStatus


class OrderItemBase(BaseModel):
    inventory_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
