from fastapi import APIRouter, Depends
from binance_config import client
from db import get_current_user

router = APIRouter(tags=["Testnet Balance"])

@router.get("/balance")
async def get_balance(current_user: dict = Depends(get_current_user)):
    account_info = client.get_account()
    balances = []

    for balance in account_info["balances"]:
        free = float(balance["free"])
        locked = float(balance["locked"])
        if free > 0 or locked > 0:
            balances.append({
                "asset": balance["asset"],
                "free": free,
                "locked": locked
            })

    return {"balances": balances}