from fastapi import FastAPI, Request
from zoneinfo import ZoneInfo
from datetime import datetime

app = FastAPI()

@app.post("/payment")
async def receive_payment(notification: Request):
    data = await notification.json()


    amount = data.get("message")

    print("Payment Message Received!")
  
    print(f"Amount: {amount}")

    rupees = int(amount.split()[-1][1:])
    time = datetime.now(ZoneInfo("Asia/Kolkata"))
    

    return {
        "message": "Payment received successfully",
        "received_data": data,
        "rupees": rupees,
        "time": time.isoformat()
    }