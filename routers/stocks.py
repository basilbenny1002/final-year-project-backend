from fastapi import APIRouter, HTTPException
from database.products import update_product_stock
from models.stock import StockUpdateRequest

router = APIRouter(prefix="/api")

@router.post("/update-stock")
async def update_stock_endpoint(request: StockUpdateRequest):
    for item in request.items:
        update_product_stock(item.name, item.quantity)
    return {"message": "Stock updated successfully"}
