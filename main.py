from fastapi import FastAPI
from routers.cart.websocket import router as websocket_router

app = FastAPI()

# Include the cart WebSocket router
app.include_router(websocket_router)
