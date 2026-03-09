from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.cart.websocket import router as cart_websocket_router
from routers.frontend.websocket import router as frontend_websocket_router
from payment_handler.payment import router as payment_router
from routers.stocks import router as stocks_router

app = FastAPI()

# Add CORS Middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the WebSocket routers
app.include_router(cart_websocket_router)
app.include_router(frontend_websocket_router)
app.include_router(payment_router)
app.include_router(stocks_router)
