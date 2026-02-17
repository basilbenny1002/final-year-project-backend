from fastapi import FastAPI
from routers.cart.websocket import router as cart_websocket_router
from routers.frontend.websocket import router as frontend_websocket_router

app = FastAPI()


@app.get("/")
def base_status():
	return {"status": "ok", "message": "ITS WORKING!!", "version": "1.0.0"}

# Include the WebSocket routers
app.include_router(cart_websocket_router)
app.include_router(frontend_websocket_router)
