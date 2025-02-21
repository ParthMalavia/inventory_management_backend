from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.controllers import inventory as inventory_controller
from app.schemas.inventory import (
    Inventory, InventoryCreate, InventoryUpdate, InventoryQuantityUpdate
)
from app.db.session import get_db
# TODO: REMOVE: from app.utils.auth import get_current_user  # Assuming this exists for auth
from app.controllers.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=Inventory)
def create_inventory(
    item: InventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return inventory_controller.create_inventory(db, item)

@router.get("/", response_model=List[Inventory])
def get_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return inventory_controller.get_inventory(db, skip=skip, limit=limit)

@router.get("/{part_number}", response_model=Inventory)
def get_inventory_item(
    part_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    item = inventory_controller.get_inventory_by_part_number(db, part_number)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{part_number}", response_model=Inventory)
def update_inventory(
    part_number: str,
    item: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_item = inventory_controller.update_inventory(db, part_number, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.patch("/{part_number}/quantity", response_model=Inventory)
def update_quantity(
    part_number: str,
    quantity_update: InventoryQuantityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_item = inventory_controller.update_quantity(db, part_number, quantity_update.quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{part_number}", response_model=Inventory)
def delete_inventory(
    part_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_item = inventory_controller.delete_inventory(db, part_number)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item

@router.get("/low-stock/", response_model=List[Inventory])
def get_low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return inventory_controller.get_low_stock_items(db)
