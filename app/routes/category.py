from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.controllers import category as category_controller
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.db.session import get_db
from app.controllers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return category_controller.create_category(db, category)

@router.get("/", response_model=List[Category])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return category_controller.get_categories(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=Category)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    category = category_controller.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_category = category_controller.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", response_model=Category)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        deleted_category = category_controller.delete_category(db, category_id)
        print( "deleted_category >>>>>>", deleted_category)
        if not deleted_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return deleted_category
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
