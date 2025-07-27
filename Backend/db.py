from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI, HTTPException, status, Depends
import os
from dotenv import load_dotenv
import asyncio
from fastapi.security import OAuth2PasswordBearer
from auth import decode_access_token
from models import User, CryptoPair, Candle, Order, Transaction, Portfolio, Cart, CreditsHistory, Cache, Transfer, CandleSyncTracker
from services.real_time_price import binance_stream  # ✅ import here
from beanie import PydanticObjectId
from scheduler import cron_historical_job, cron_settle_limit_orders
import json
from services.session_store import get_session
# from chatbot.symbol_extractor import load_symbols_from_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
DATABASE_NAME = "final_project_nse"

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(mongo_uri)
    db = client[DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=[User, CryptoPair, Candle, Order, Transaction, Portfolio, Cart, CreditsHistory, Cache, Transfer, CandleSyncTracker]
    )

    # await load_symbols_from_db()
    binance_task = asyncio.create_task(binance_stream())
    candle_cron_task = asyncio.create_task(cron_historical_job())
    settle_cron_task = asyncio.create_task(cron_settle_limit_orders())

    yield

    binance_task.cancel()
    candle_cron_task.cancel()
    settle_cron_task.cancel() 
    client.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject")

    # ✅ Check session store
    session = await get_session(user_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalidated")

    user = await User.get(PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

from typing import Optional, Any

client: Any = None

async def init_db_for_worker():
    global client
    if not client:
        client = AsyncIOMotorClient(mongo_uri)

    db = client[DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=[
            User, CryptoPair, Candle, Order, Transaction, Portfolio,
            Cart, CreditsHistory, Cache, Transfer, CandleSyncTracker
        ]
    )