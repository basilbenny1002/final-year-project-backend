from pydantic import BaseModel
from typing import List

class StockItem(BaseModel):
    name: str
    quantity: int

class StockUpdateRequest(BaseModel):
    cart_id: str
    items: List[StockItem]
