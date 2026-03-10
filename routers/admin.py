from fastapi import APIRouter

from database.products import get_all_stocks, get_all_transactions, get_recent_transactions
from models.admin import StocksResponse, TransactionsResponse

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stocks", response_model=StocksResponse)
async def get_stocks_endpoint() -> StocksResponse:
    return {"stocks": get_all_stocks()}


@router.get("/transactions", response_model=TransactionsResponse)
async def get_transactions_endpoint() -> TransactionsResponse:
    return {"transactions": get_all_transactions()}


@router.get("/transactions/recent", response_model=TransactionsResponse)
async def get_recent_transactions_endpoint() -> TransactionsResponse:
    return {"transactions": get_recent_transactions(5)}
