from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    fulfilled = "fulfilled"
    canceled = "canceled"
