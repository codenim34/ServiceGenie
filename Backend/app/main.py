"""
FastAPI application main file.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.db import connect_to_mongo, close_mongo_connection
from app.core.firebase import initialize_firebase
from app.routes import auth_routes, product_routes, order_routes, owner_routes, agent_routes

# Initialize FastAPI app
app = FastAPI(
    title="ServiceGenie API",
    description="AI-powered commerce platform API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(product_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(order_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(owner_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(agent_routes.router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    # Initialize Firebase
    try:
        initialize_firebase()
        print("✅ Firebase initialized")
    except Exception as e:
        print(f"⚠️ Firebase initialization warning: {e}")
    
    # Connect to MongoDB
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    await close_mongo_connection()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ServiceGenie API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

