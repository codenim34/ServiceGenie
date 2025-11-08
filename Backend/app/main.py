"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.core.memory_db import db
from app.core.auth import create_access_token, get_current_user

app = FastAPI(title="ServiceGenie API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Product models
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

# Order models
class OrderCreate(BaseModel):
    product_id: str
    quantity: int

# Auth endpoints
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    if db.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = db.create_user(user_data.dict())
    access_token = create_access_token({"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = db.get_user_by_email(user_data.email)
    if not user or user["password"] != user_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Product endpoints
@app.post("/products")
async def create_product(product: ProductCreate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db.create_product(product.dict())

@app.get("/products")
async def list_products():
    return db.list_products()

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
async def update_product(product_id: str, product: ProductUpdate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    updated_product = db.update_product(product_id, product.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Order endpoints
@app.post("/orders")
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    product = db.get_product(order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    order_data = {
        "user_id": current_user["id"],
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": product["price"] * order.quantity,
    }
    
    return db.create_order(order_data)

@app.get("/orders")
async def list_orders(current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db.list_user_orders(current_user["id"])

