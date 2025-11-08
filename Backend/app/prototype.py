from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="ServiceGenie API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for prototype/dev. Restrict in production.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
db = {
    "products": [],
    "users": [],
    "orders": []
}

# Models
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    image_url: Optional[str] = None

class User(BaseModel):
    id: Optional[int] = None
    email: str
    business_name: str

class Order(BaseModel):
    id: Optional[int] = None
    product_id: int
    quantity: int
    customer_email: str
    status: str = "pending"

# Product endpoints
@app.get("/api/products", response_model=List[Product])
async def get_products():
    return db["products"]

@app.post("/api/products", response_model=Product)
async def create_product(product: Product):
    product.id = len(db["products"]) + 1
    db["products"].append(product.dict())
    return product

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in db["products"]:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# User endpoints
@app.post("/api/users", response_model=User)
async def create_user(user: User):
    user.id = len(db["users"]) + 1
    db["users"].append(user.dict())
    return user

@app.get("/api/users", response_model=List[User])
async def get_users():
    return db["users"]

# Order endpoints
@app.post("/api/orders", response_model=Order)
async def create_order(order: Order):
    order.id = len(db["orders"]) + 1
    db["orders"].append(order.dict())
    return order

@app.get("/api/orders", response_model=List[Order])
async def get_orders():
    return db["orders"]

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# Simple mock AI agent endpoints for prototype
@app.post("/api/agent/chat")
async def chat_with_agent(message: dict):
    """Accepts { content: str, owner_id?: str } and returns a mock reply."""
    content = message.get("content") if isinstance(message, dict) else None
    if not content:
        raise HTTPException(status_code=400, detail="Missing content")

    # Simple echo reply with a friendly message and no products
    reply_text = f"You said: {content}. (This is a prototype reply.)"
    return {"reply": reply_text, "products": []}


@app.get("/api/agent/chat/history")
async def chat_history(owner_id: Optional[str] = None):
    """Return empty history for prototype."""
    return []

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)