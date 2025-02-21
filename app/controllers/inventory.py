from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate

def create_inventory(db: Session, item: InventoryCreate):
    db_item = Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Inventory).offset(skip).limit(limit).all()

def get_inventory_by_part_number(db: Session, part_number: str):
    return db.query(Inventory).filter(Inventory.part_number == part_number).first()

def update_inventory(db: Session, part_number: str, item: InventoryUpdate):
    db_item = get_inventory_by_part_number(db, part_number)
    if not db_item:
        return None
    update_data = item.dict(exclude_unset=True)  # Only update provided fields
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_quantity(db: Session, part_number: str, quantity: int):
    db_item = get_inventory_by_part_number(db, part_number)
    if not db_item:
        return None
    db_item.quantity = quantity
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_inventory(db: Session, part_number: str):
    db_item = get_inventory_by_part_number(db, part_number)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def get_low_stock_items(db: Session):
    return db.query(Inventory).filter(Inventory.quantity <= Inventory.low_stock_threshold).all()
