from fastapi import APIRouter, HTTPException

from database.products import get_all_stocks, get_all_transactions, get_recent_transactions, add_or_update_product_stock
from models.admin import StocksResponse, TransactionsResponse, AdminStockUpdateRequest, AdminStockUpdateResponse

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stocks", response_model=StocksResponse)
async def get_stocks_endpoint() -> StocksResponse:
    return {"stocks": get_all_stocks()}


@router.post("/stocks/update", response_model=AdminStockUpdateResponse)
async def update_stock_endpoint(request: AdminStockUpdateRequest) -> AdminStockUpdateResponse:
    result = add_or_update_product_stock(
        request.product_id, 
        request.name, 
        request.price, 
        request.number
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return {"success": True, "message": result.get("message")}


@router.get("/transactions", response_model=TransactionsResponse)
async def get_transactions_endpoint() -> TransactionsResponse:
    return {"transactions": get_all_transactions()}


@router.get("/transactions/recent", response_model=TransactionsResponse)
async def get_recent_transactions_endpoint() -> TransactionsResponse:
    return {"transactions": get_recent_transactions(5)}
