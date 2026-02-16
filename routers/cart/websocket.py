import json
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# Helper function to check if the cart ID is in our JSON file
def is_cart_valid(cart_id: str) -> bool:
    """
    Returns True if the cart_id exists in carts.json, otherwise False.
    parameter cart_id: The ID of the cart to validate.
    return: True if valid, False if not.
    """
    if not os.path.exists("carts.json"):
        print("carts.json not found!", flush=True)
        return False
        
    with open("carts.json", "r") as file:
        data = json.load(file)
        return cart_id in data.get("valid_carts", [])

@router.websocket("/ws/{cart_id}")
async def websocket_endpoint(websocket: WebSocket, cart_id: str):
    """
    Websocket endpoint for cart connections. Validates the cart ID against a JSON file before accepting the connection.
    parameter websocket: The WebSocket connection object.
    """
    # 1. Check the cart ID against the JSON before accepting
    if not is_cart_valid(cart_id):
        print(f"Connection rejected: Cart '{cart_id}' is not in the system.", flush=True)
        await websocket.close(code=1008, reason="Invalid Cart ID")
        return
    
    # 2. Accept the connection if valid
    await websocket.accept()
    print(f"Cart '{cart_id}' connected successfully!", flush=True)
    
    try:
        # 3. Listen for scanned items from the ESP32
        while True:
            item_data = await websocket.receive_text()
            print(f"[Cart: {cart_id}] Scanned Item: {item_data}", flush=True)
            
    except WebSocketDisconnect:
        print(f"Cart '{cart_id}' disconnected.", flush=True)
