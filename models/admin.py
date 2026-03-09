from typing import List

from pydantic import BaseModel


class StockRecord(BaseModel):
    product_id: int
    name: str
    price: float
    stock_count: int


class TransactionRecord(BaseModel):
    id: int
    purchase_id: str
    product_name: str
    price: float
    quantity: int
    created_at: str


class StocksResponse(BaseModel):
    stocks: List[StockRecord]


class TransactionsResponse(BaseModel):
    transactions: List[TransactionRecord]
