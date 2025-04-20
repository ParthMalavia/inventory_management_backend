from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, index=True, nullable=False)  # Unique identifier for parts
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False)
    low_stock_threshold = Column(Integer, default=10)  # Threshold for low-stock alerts
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # Foreign key to Category
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to access category details
    category = relationship("Category")
    # category = relationship("Category", back_populates="items")

# # Add back_populates to Category (we'll define it below)
# Category.items = relationship("Inventory", back_populates="category")