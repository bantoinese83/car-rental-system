# Car Rental System

## Overview

This project is a car rental system built with FastAPI. It includes features for user authentication, car management, booking, and payment processing.

## Features

- User Registration and Authentication
- Car Management (CRUD operations)
- Booking Management
- Payment Processing with Stripe
- Rate Limiting and Middleware for enhanced security and performance

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/bantoinese83/car-rental-system.git
    cd car-rental-system
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    # Edit the .env file with your configuration
    ```

5. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

## Usage

### API Endpoints

- **Authentication**
  - `POST /api/v1/auth/register`: Register a new user
  - `POST /api/v1/auth/login`: Login and get an access token

- **Cars**
  - `POST /api/v1/cars/`: Create a new car (Admin only)
  - `GET /api/v1/cars/{car_id}`: Get car details
  - `PUT /api/v1/cars/{car_id}`: Update car details (Admin only)
  - `DELETE /api/v1/cars/{car_id}`: Delete a car (Admin only)
  - `GET /api/v1/cars/`: Search for cars

- **Bookings**
  - `POST /api/v1/bookings/`: Create a new booking
  - `GET /api/v1/bookings/{booking_id}`: Get booking details
  - `PUT /api/v1/bookings/{booking_id}`: Update booking details
  - `DELETE /api/v1/bookings/{booking_id}`: Delete a booking

- **Payments**
  - `POST /api/v1/payments/create-payment-intent`: Create a payment intent
  - `POST /api/v1/payments/webhook`: Handle Stripe webhook events

- **Pricing**
  - `GET /api/v1/pricing`: Get pricing details for a car
  - `POST /api/v1/pricing`: Create pricing for a car (Admin only)
  - `PUT /api/v1/pricing/{car_id}`: Update pricing for a car (Admin only)

- **Users**
  - `GET /api/v1/users/`: Get a list of users (Admin only)
  - `GET /api/v1/users/me`: Get current user details
  - `GET /api/v1/users/{user_id}`: Get user details (Admin only)
  - `PUT /api/v1/users/{user_id}`: Update user details (Admin only)
  - `DELETE /api/v1/users/{user_id}`: Delete a user (Admin only)

- **Agent**
  - `POST /api/v1/agent/interactive_chat_agent`: Interactive chat agent for car rentals
## Running Tests

To run the tests, use the following command:
```sh
pytest