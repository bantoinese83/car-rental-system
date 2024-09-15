import uuid

from app.models.user import Role
from app.models.user import User


# tests/test_auth.py

def test_register_user(test_client):
    unique_username = f"testuser_{uuid.uuid4()}"
    unique_email = f"{unique_username}@example.com"
    response = test_client.post("/api/v1/auth/register", json={
        "username": unique_username,
        "password": "testpassword",
        "email": unique_email,
        "full_name": "Test User",
        "phone_number": "1234567890",
        "role": Role.ADMIN,  # Ensure the user is an admin
        "is_active": True  # Add the missing is_active field
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert "message" in response_json
    assert response_json["message"] == "User registered successfully"


def test_login_for_access_token(test_client, test_user):
    response = test_client.post("/api/v1/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_read_users_me(test_client, test_user):
    # First, login to get the token
    response = test_client.post("/api/v1/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None, "Token should not be None"

    # Print the token for debugging
    print(f"Token: {token}")

    # Use the token to access the protected route
    response = test_client.get("/api/v1/users/me", headers={
        "Authorization": f"Bearer {token}"
    })

    # Print the response for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == test_user.id
    assert "username" in response.json()
    assert response.json()["username"] == test_user.username
    assert "email" in response.json()
    assert response.json()["email"] == test_user.email
    assert "full_name" in response.json()
    assert response.json()["full_name"] == test_user.full_name
    assert "phone_number" in response.json()
    assert response.json()["phone_number"] == test_user.phone_number
    assert "role" in response.json()
    assert response.json()["role"] == test_user.role
    assert "is_active" in response.json()
    assert response.json()["is_active"] == test_user.is_active


def test_register_user_with_existing_username(test_client, db_session, reset_rate_limiter):
    # Ensure the user does not already exist
    existing_user = db_session.query(User).filter_by(email="testuser@example.com").first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    # Register the user for the first time
    response = test_client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "is_active": True
    })
    assert response.status_code == 200

    # Reset the rate limiter
    reset_rate_limiter.requests_this_minute = 0
    reset_rate_limiter.tokens_this_minute = 0
    reset_rate_limiter.requests_today = 0

    # Attempt to register the user again with the same email
    response = test_client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "is_active": True
    })
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Email already registered"


def test_login_with_invalid_credentials(test_client):
    # Reset or mock the rate limiter here if necessary
    response = test_client.post("/api/v1/auth/login", data={
        "username": "invaliduser@example.com",
        "password": "invalidpassword"
    })
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect username or password"
