from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
import stripe
from app.core.config import settings
from app.core.database import get_database
from app.core.security import get_current_user
from app.models.user import UserInDB
from bson import ObjectId
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    orderId: str

class PaymentIntentResponse(BaseModel):
    clientSecret: str
    publishableKey: str

@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    payment_request: PaymentIntentRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Create a Stripe payment intent for an order.
    """
    db = get_database()
    
    if not ObjectId.is_valid(payment_request.orderId):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    # Get order
    order = await db.orders.find_one({"_id": ObjectId(payment_request.orderId)})
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order
    if order["userId"] != current_user.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to pay for this order"
        )
    
    # Check if already paid
    if order["paymentStatus"] == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already paid"
        )
    
    try:
        # Create Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order["totalAmount"] * 100),  # Convert to cents
            currency="usd",
            metadata={
                "orderId": str(order["_id"]),
                "userId": current_user.uid
            }
        )
        
        return PaymentIntentResponse(
            clientSecret=payment_intent.client_secret,
            publishableKey=settings.STRIPE_SECRET_KEY.split("_")[0] + "_publishable"  # Mock for now
        )
    
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order_id = payment_intent["metadata"]["orderId"]
        
        # Update order payment status
        db = get_database()
        await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "paymentStatus": "paid",
                    "status": "processing",
                    "updatedAt": datetime.utcnow()
                }
            }
        )
    
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        order_id = payment_intent["metadata"]["orderId"]
        
        # Update order payment status
        db = get_database()
        await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "paymentStatus": "failed",
                    "updatedAt": datetime.utcnow()
                }
            }
        )
    
    return {"status": "success"}
