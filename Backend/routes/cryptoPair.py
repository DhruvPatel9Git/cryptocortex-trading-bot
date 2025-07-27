from fastapi import APIRouter, Query, Depends
from fetch_binance.fetch_cryptoPair import fetch_and_store_binance_symbols
from typing import Optional
from models import CryptoPair
from db import get_current_user

router = APIRouter(tags=["Cryptos"])

@router.post("/sync_binance_symbols")
async def sync_binance_symbols(current_user: dict = Depends(get_current_user)):
    await fetch_and_store_binance_symbols()
    return {"status": "sync complete"}

@router.get("/cryptos")
async def get_cryptos(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by symbol or base_asset")
):
    query = {}
    if search:
        query = {
            "$or": [
                {"symbol": {"$regex": search, "$options": "i"}},
                {"base_asset": {"$regex": search, "$options": "i"}}
            ]
        }

    pairs = await CryptoPair.find(query).skip(skip).limit(limit).to_list()
    total = await CryptoPair.find(query).count()

    return {
        "items": [{"symbol": p.symbol, "base_asset": p.base_asset} for p in pairs],
        "total": total
    }

@router.get("/cryptos/search")
async def search_cryptos(query: str = Query(..., description="Search by symbol or base asset")):
    search_filter = {
        "$or": [
            {"symbol": {"$regex": query, "$options": "i"}},
            {"base_asset": {"$regex": query, "$options": "i"}}
        ]
    }

    results = await CryptoPair.find(search_filter).to_list()
    return [
        {"symbol": pair.symbol, "base_asset": pair.base_asset}
        for pair in results
    ]

@router.get("/cryptos/all")
async def get_all_cryptos():
    pairs = await CryptoPair.find_all().to_list()
    return [p.symbol for p in pairs]