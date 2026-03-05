from fastapi import APIRouter
from models.payment import NotificationPayload

router = APIRouter()


@router.post("/") 
async def receive_payment_notification(data: NotificationPayload):
    print("----- New Notification Received -----", flush=True)
    print(f"Title:   {data.title}", flush=True)
    print(f"Content: {data.content}", flush=True)
    
    # You can now parse 'data.content' to extract amounts, names, etc.
    
    return {"message": "Notification received successfully"}