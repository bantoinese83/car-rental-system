import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db_session
from app.core.rate_limiter import RateLimiter
from app.models.message import Message as MessageModel
from app.schemas.booking import BookingCreate
from app.schemas.messages import Message
from app.services.chatbot_service import handle_inquire_rentals, handle_book_rental, handle_cancel_booking, \
    handle_search_cars

# Create a router with versioning
gemini_router = APIRouter()

# Initialize the rate limiter
rate_limiter = RateLimiter(max_requests_per_minute=5, max_tokens_per_minute=10, max_requests_per_day=100)


@gemini_router.post("/interactive_chat_agent", summary="Interactive Chat Agent",
                    description="Car rental chatbot agent for interactive chat.")
async def interactive_chat(messages: List[Message], db: Session = Depends(get_db_session)):
    try:
        # Check rate limit
        if not rate_limiter.can_proceed(tokens=1):
            logger.warning("Rate limit exceeded")
            raise HTTPException(status_code=429, detail="Too many requests")

        # Log the received messages
        logger.debug(f"Received messages: {messages}")

        # Validate roles
        for message in messages:
            if message.role not in ["customer", "agent"]:
                logger.error(f"Invalid role found: {message.role}")
                raise HTTPException(status_code=400, detail="Please use a valid role: customer, agent.")

        # Log the validated messages
        logger.debug(f"Validated messages: {messages}")

        # Store messages in the database
        for message in messages:
            try:
                db_message = MessageModel(
                    role=message.role,
                    parts=json.dumps(message.parts),
                    intent=message.intent,
                    timestamp=datetime.utcnow()
                )
                db.add(db_message)
            except (TypeError, ValueError) as e:
                logger.error(f"Error encoding message parts to JSON: {e}")
                raise HTTPException(status_code=400, detail="Invalid message parts format")
        db.commit()

        # Determine the intent and handle accordingly
        last_message = messages[-1]
        intent = last_message.intent

        logger.debug(f"Last message intent: {intent}")
        logger.debug(f"Last message parts: {last_message.parts}")

        if intent == "inquire_rentals":
            response_data = handle_inquire_rentals(db)
        elif intent == "book_rental":
            booking_data = BookingCreate(**last_message.parts)
            logger.debug(f"Booking data: {booking_data}")
            response_data = handle_book_rental(db, booking_data)
        elif intent == "cancel_booking":
            booking_id = int(last_message.parts.get("booking_id"))
            logger.debug(f"Booking ID to cancel: {booking_id}")
            response_data = handle_cancel_booking(db, booking_id)
        elif intent == "search_cars":
            search_criteria = last_message.parts
            logger.debug(f"Search criteria: {search_criteria}")
            response_data = handle_search_cars(db, search_criteria)
        else:
            logger.warning(f"Unknown intent: {intent}")
            response_data = {"message": "Unknown intent"}

        # Log the response data
        logger.debug(f"Response data: {response_data}")

        return JSONResponse(content=jsonable_encoder({'response': response_data}), status_code=200)
    except ValueError as ve:
        logger.error(f"Value error in interactive chat: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in interactive chat: {e}")
        raise HTTPException(status_code=500, detail="Error in interactive chat")
