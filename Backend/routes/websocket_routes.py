from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.real_time_price import clients

router = APIRouter()

@router.websocket("/ws/prices")
async def websocket_price(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected")
    clients.append(websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                pass
    except WebSocketDisconnect:
        print("⚠️ Client disconnected")
        clients.remove(websocket)
