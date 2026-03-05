import json
import os
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


# Helper function to check if the cart ID is in our JSON file
def is_cart_valid(cart_id: str) -> bool:
    if not os.path.exists("carts.json"):
        print("carts.json not found!", flush=True)
        return False

    with open("carts.json", "r") as file:
        data = json.load(file)
        return cart_id in data.get("valid_carts", [])


class FrontendConnectionManager:
    def __init__(self) -> None:
        self._connections: Dict[str, WebSocket] = {}

    async def connect(self, cart_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[cart_id] = websocket

    def disconnect(self, cart_id: str) -> None:
        self._connections.pop(cart_id, None)

    async def send_item(self, cart_id: str, item_name: str, price: float) -> bool:
        websocket = self._connections.get(cart_id)
        if not websocket:
            return False

        await websocket.send_json({"item_name": item_name, "price": price})
        return True


manager = FrontendConnectionManager()


@router.websocket("/frontend/ws/{cart_id}")
async def frontend_websocket_endpoint(websocket: WebSocket, cart_id: str) -> None:
    # 1. Check the cart ID against the JSON before accepting
    if not is_cart_valid(cart_id):
        print(f"Connection rejected: Cart '{cart_id}' is not in the system.", flush=True)
        await websocket.close(code=1008, reason="Invalid Cart ID")
        return

    # 2. Accept the connection if valid
    await manager.connect(cart_id, websocket)
    print(f"Frontend for cart '{cart_id}' connected successfully!", flush=True)

    try:
        # Keep the connection alive; listen for messages if needed
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(cart_id)
        print(f"Frontend for cart '{cart_id}' disconnected.", flush=True)


async def send_item_to_frontend(cart_id: str, item_name: str, price: float) -> bool:
    """
    Send an item payload to the connected frontend for a specific cart.
    Returns True if a frontend was connected and the message was sent.
    """
    return await manager.send_item(cart_id, item_name, price)
