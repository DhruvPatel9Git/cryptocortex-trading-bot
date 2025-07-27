
from models import Candle

async def get_candlestick_context(symbol, start_date, end_date):
    query = {"symbol": symbol}
    query["candle_time"] = {"$gte": start_date, "$lte": end_date}

    candles = await Candle.find(query).sort("candle_time").to_list()

    if not candles:
        return None

    lines = []
    for c in candles:
        lines.append(
            f"Symbol: {c.symbol}, Date: {c.candle_time.strftime('%Y-%m-%d')} - Open: {c.open}, High: {c.high}, Low: {c.low}, Close: {c.close}, Volume: {c.volume}"
        )

    return "\n".join(lines)
