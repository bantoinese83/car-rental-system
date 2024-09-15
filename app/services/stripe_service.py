import stripe
from fastapi import HTTPException

from app.core.app_config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_payment_intent(amount: int, currency: str = "usd"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return intent
    except stripe.error.StripeError as e:
        # Don't catch and raise a new HTTPException here
        raise  # Let the exception bubble up


# app/services/stripe_service.py

# app/services/stripe_service.py

def handle_webhook_event(event):
    event_type = event.get("type")
    data = event.get("data", {})
    if not data:
        raise KeyError("data")

    # Process the event based on its type
    if event_type == "payment_intent.succeeded":
        # Handle the payment intent succeeded event
        pass
    # Add other event types as needed
