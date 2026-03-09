from fastapi import APIRouter

from database.products import get_all_stocks, get_all_transactions, get_recent_transactions

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stocks")
async def get_stocks_endpoint():
    return {"stocks": get_all_stocks()}


@router.get("/transactions")
async def get_transactions_endpoint():
    return {"transactions": get_all_transactions()}


@router.get("/transactions/recent")
async def get_recent_transactions_endpoint():
    return {"transactions": get_recent_transactions(5)}
