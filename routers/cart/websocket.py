import json
import os
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from database.products import get_product
from routers.frontend.websocket import send_item_to_frontend

router = APIRouter()

def is_cart_valid(cart_id: str) -> bool:
    if not os.path.exists("carts.json"):
        print("carts.json not found!", flush=True)
        return False
        
    with open("carts.json", "r") as file:
        data = json.load(file)
        return cart_id in data.get("valid_carts", [])


class CartConnectionManager:
    def __init__(self) -> None:
        self._connections: Dict[str, WebSocket] = {}

    async def connect(self, cart_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[cart_id] = websocket

    def disconnect(self, cart_id: str) -> None:
        self._connections.pop(cart_id, None)

    async def send_unlock(self, cart_id: str) -> bool:
        websocket = self._connections.get(cart_id)
        if not websocket:
            return False

        await websocket.send_json({"command": "unlock"})
        return True


manager = CartConnectionManager()

@router.websocket("/ws/{cart_id}")
async def websocket_endpoint(websocket: WebSocket, cart_id: str) -> None:
    # 1. Check the cart ID against the JSON before accepting
    if not is_cart_valid(cart_id):
        print(f"Connection rejected: Cart '{cart_id}' is not in the system.", flush=True)
        await websocket.close(code=1008, reason="Invalid Cart ID")
        return
    
    # 2. Accept the connection if valid
    await manager.connect(cart_id, websocket)
    print(f"Cart '{cart_id}' connected successfully!", flush=True)
    
    try:
        # 3. Listen for scanned items from the ESP32
        while True:
            item_data = await websocket.receive_text()
            print(f"[Cart: {cart_id}] Scanned Item: {item_data}", flush=True)
            item_info = get_product(int(item_data))
            send_item_to_frontend(cart_id, item_info["name"], item_info["price"])
            
    except WebSocketDisconnect:
        manager.disconnect(cart_id)
        print(f"Cart '{cart_id}' disconnected.", flush=True)


async def send_unlock_to_cart(cart_id: str) -> bool:
    """Send an unlock command to a specific cart if connected."""
    return await manager.send_unlock(cart_id)
