from fetch_binance.fetch_ohlc import fetch_historical_data
from fetch_binance.background_jobs import settle_filled_limit_orders
import asyncio

async def cron_historical_job():
    while True:
        try:
            await fetch_historical_data("1d", 30)  
        except Exception as e:
            print("Error in cron job:", e)
        await asyncio.sleep(3600 * 6) 

async def cron_settle_limit_orders():
    while True:
        try:
            await settle_filled_limit_orders()
        except Exception as e:
            print("Error in settlement cron job:", e)
        await asyncio.sleep(300)  

    