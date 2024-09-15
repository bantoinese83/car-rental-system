from unittest.mock import patch

import stripe


def test_create_payment_intent_success(test_client):
    with patch('app.services.stripe_service.create_payment_intent') as mock_create_payment_intent:
        mock_create_payment_intent.return_value = type('obj', (object,),
                                                       {'id': 'pi_123', 'client_secret': 'secret_123'})

        response = test_client.post("/api/v1/payments/create-payment-intent", json={"amount": 1000})
        print(response.json())  # Print the response content for debugging
        assert response.status_code == 200


def test_create_payment_intent_invalid_amount(test_client):
    response = test_client.post("/api/v1/payments/create-payment-intent", json={"amount": 0})
    assert response.status_code == 400


def test_create_payment_intent_stripe_error(test_client):
    with patch('stripe.PaymentIntent.create') as mock_create_payment_intent:
        mock_create_payment_intent.side_effect = stripe.error.StripeError("Stripe error")

        response = test_client.post("/api/v1/payments/create-payment-intent", json={"amount": 1000})

        assert response.status_code == 500
        assert response.json()["detail"] == "Stripe error"


def test_stripe_webhook_invalid_signature(test_client):
    payload = {"id": "evt_123", "type": "payment_intent.succeeded"}
    response = test_client.post("/api/v1/payments/webhook", json=payload,
                                headers={"stripe-signature": "invalid_signature"})
    assert response.status_code == 400


def test_stripe_webhook_success(test_client):
    payload = '{"id": "evt_123", "type": "payment_intent.succeeded", "data": {"object": {"id": "pi_123", "amount": 1000}}}'
    sig_header = "valid_signature"

    with patch("stripe.Webhook.construct_event") as mock_construct_event:
        mock_construct_event.return_value = {
            "id": "evt_123",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_123", "amount": 1000}}
        }
        response = test_client.post("/api/v1/payments/webhook", data=payload, headers={"stripe-signature": sig_header})
        assert response.status_code == 200


def test_stripe_webhook_invalid_payload(test_client):
    payload = 'invalid_payload'
    sig_header = "invalid_signature"

    with patch("stripe.Webhook.construct_event") as mock_construct_event:
        mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
            "Invalid signature", "header"
        )
        response = test_client.post("/api/v1/payments/webhook", data=payload, headers={"stripe-signature": sig_header})
        assert response.status_code == 400
