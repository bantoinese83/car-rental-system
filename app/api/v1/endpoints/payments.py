# app/api/v1/endpoints/payments.py

import stripe
from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from app.core.app_config import settings
from app.schemas.payment import PaymentRequest
from app.services.stripe_service import create_payment_intent, handle_webhook_event

router = APIRouter()


@router.post("/create-payment-intent")
async def create_payment(payment_request: PaymentRequest, request: Request):
    amount = payment_request.amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    try:
        intent = create_payment_intent(amount)
        logger.info(f"Payment intent created: {intent.id}")
        return {"client_secret": intent.client_secret}
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    if not sig_header:
        logger.warning("Missing stripe-signature header")
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        logger.debug(f"Webhook event received: {event}")
        handle_webhook_event(event)
        logger.info(f"Webhook event handled: {event['type']}")
    except KeyError as e:
        logger.error(f"Error handling webhook event: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key in event: {e}")
    except Exception as e:
        logger.error(f"Error handling webhook event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"status": "success"}