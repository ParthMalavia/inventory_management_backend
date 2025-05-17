from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    fulfilled = "fulfilled"
    canceled = "canceled"


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"
