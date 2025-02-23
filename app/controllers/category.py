from sqlalchemy.orm import Session
from app.models.catagory import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.inventory import Inventory


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    # Check if category has associated items
    if db.query(Inventory).filter(Inventory.category_id == category_id).count() > 0:
        raise ValueError("Cannot delete category with associated inventory items")
    db.delete(db_category)
    db.commit()
    return db_category
