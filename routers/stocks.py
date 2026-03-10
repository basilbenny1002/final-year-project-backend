from fastapi import APIRouter, HTTPException
from database.products import update_product_stock, get_product_price, insert_transaction
from models.stock import StockUpdateRequest
import uuid

router = APIRouter(prefix="/api")

@router.post("/update-stock")
async def update_stock_endpoint(request: StockUpdateRequest):
    purchase_id = str(uuid.uuid4())
    
    for item in request.items:
        # Update stock
        update_product_stock(item.name, item.quantity)
        
        # Record transaction
        price = get_product_price(item.name)
        total_price = price * item.quantity
        insert_transaction(purchase_id, item.name, total_price, item.quantity)
        
    return {"message": "Stock updated and transaction recorded successfully", "purchase_id": purchase_id}
