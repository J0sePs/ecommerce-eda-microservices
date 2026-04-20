from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class OrderItemSchema(BaseModel):
    product_id: str
    product_name: str
    sku: str
    unit_price: float
    quantity: int

class OrderCreateCommand(BaseModel):
    user_id: str
    items: List[OrderItemSchema]
    shipping_address: dict

    model_config = ConfigDict(extra='forbid')
