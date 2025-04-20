from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.controllers.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/status/{status}", response_model=list[OrderResponse])
def get_orders_by_status(
    status: OrderStatus,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Order).filter(Order.status == status).all()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = Order(customer_id=order_data.customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_data.items:
        inventory_item = (
            db.query(Inventory).filter(Inventory.id == item.inventory_id).first()
        )
        if not inventory_item:
            raise HTTPException(
                status_code=404, detail=f"Inventory item {item.inventory_id} not found"
            )
        if inventory_item.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {inventory_item.part_number}",
            )
        inventory_item.quantity -= item.quantity

        db_item = OrderItem(order_id=order.id, **item.model_dump())
        db.add(db_item)

    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if update_data.status:
        order.status = update_data.status
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
