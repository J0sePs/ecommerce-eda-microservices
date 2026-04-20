import uuid
from typing import List
from datetime import datetime

from domain.value_objects.order_status import OrderStatus

class OrderItem:
    def __init__(self, product_id: str, product_name: str, sku: str, unit_price: float, quantity: int):
        self.id = str(uuid.uuid4())
        self.product_id = product_id
        self.product_name = product_name
        self.sku = sku
        self.unit_price = unit_price
        self.quantity = quantity
        self.subtotal = unit_price * quantity

class Order:
    def __init__(self, user_id: str, items: List[OrderItem], shipping_address: dict, currency: str = "USD"):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.status = OrderStatus.PENDING
        self.items = items
        self.total_amount = sum(item.subtotal for item in items)
        self.currency = currency
        self.shipping_address = shipping_address
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @classmethod
    def create(cls, user_id: str, items: List[OrderItem], shipping_address: dict):
        return cls(user_id=user_id, items=items, shipping_address=shipping_address)

    def to_event_dict(self):
        return {
            "order_id": self.id,
            "user_id": self.user_id,
            "status": self.status.value,
            "total": float(self.total_amount),
            "currency": self.currency,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "sku": item.sku,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price)
                } for item in self.items
            ],
            "shipping_address": self.shipping_address
        }

    def cancel(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError("Only PENDING orders can be cancelled.")
        self.status = OrderStatus.CANCELLED

    def confirm(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError("Only PENDING orders can be confirmed.")
        self.status = OrderStatus.CONFIRMED

    def pay(self):
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Only CONFIRMED orders can be paid.")
        self.status = OrderStatus.PAID
