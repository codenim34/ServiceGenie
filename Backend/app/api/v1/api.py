from fastapi import APIRouter
from app.api.v1.endpoints import products, orders, users, categories, payment
from app.routes import agent_routes

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])

# Include AI agent routes
api_router.include_router(agent_routes.router, prefix="/agent", tags=["agent"])
