import asyncio
import json
import websockets
from models import CryptoPair
from beanie import PydanticObjectId

clients = []

async def build_stream_url():
    crypto_pairs = await CryptoPair.find_all().to_list()
    symbols = [pair.symbol.lower() for pair in crypto_pairs]
    if not symbols:
        return None
    stream_path = "/".join([f"{s}@ticker" for s in symbols])
    return f"wss://stream.binance.com:9443/stream?streams={stream_path}"

async def binance_stream():
    while True:
        try:
            print("🌐 Binance stream connecting...")
            url = await build_stream_url()
            if not url:
                print("⚠️ No symbols found in DB to stream. Retrying in 30s.")
                await asyncio.sleep(30)
                continue

            async with websockets.connect(url) as websocket:
                print(f" Connected to Binance (stream established).")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    payload = data.get("data")

                    if payload:
                        for client in clients.copy():
                            try:
                                await client.send_text(json.dumps(payload))
                            except Exception as e:
                                print("❌ Error sending to client:", e)
                                clients.remove(client)

        except Exception as e:
            print(f"❌ Binance stream error: {e}")
            print("🔁 Reconnecting in 10 seconds...")
            await asyncio.sleep(10)
