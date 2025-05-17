from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Enum

from app.db.session import Base
from app.utils.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(LargeBinary)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.staff)
