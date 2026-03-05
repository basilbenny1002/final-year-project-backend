from fastapi import APIRouter
from models.payment import NotificationPayload
from routers.frontend.websocket import send_payment_success_to_frontend

router = APIRouter()


@router.post("/") 
async def receive_payment_notification(data: NotificationPayload):
    print("----- New Notification Received -----", flush=True)
    print(f"Title:   {data.title}", flush=True)
    print(f"Content: {data.content}", flush=True)
    
    # Forward payment success to the frontend if content (cart_id) is present
    if data.content:
        cart_id = data.content.strip()
        await send_payment_success_to_frontend(cart_id)
        print(f"Forwarded payment notification to cart: {cart_id}", flush=True)
    
    return {"message": "Notification received successfully"}