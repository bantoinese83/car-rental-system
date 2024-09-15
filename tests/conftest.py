import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.rate_limiter import RateLimiter
from app.core.security import get_password_hash
from app.db.session import engine, Base
from app.main import app
from app.models.model_enums import Role
from app.models.user import User


@pytest.fixture
def reset_rate_limiter():
    rate_limiter = RateLimiter(max_requests_per_minute=5, max_tokens_per_minute=10, max_requests_per_day=100)
    rate_limiter.requests_this_minute = 0
    rate_limiter.tokens_this_minute = 0
    rate_limiter.requests_today = 0
    return rate_limiter


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables before running tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture
def db_session():
    session = Session(bind=engine)
    yield session
    session.close()


@pytest.fixture
def test_user(db_session: Session):
    existing_user = db_session.query(User).filter_by(username="testuser@example.com").first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    user = User(
        username="testuser@example.com",
        email="testuser@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        phone_number="1234567890",
        role=Role.ADMIN,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_booking_data():
    return {
        "start_time": "2023-10-01T10:00:00",
        "end_time": "2023-10-01T12:00:00",
        "car_id": 1,
        "user_id": 1
    }

@pytest.fixture
def auth_headers(test_client: TestClient, test_user: User):
    response = test_client.post("/api/v1/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None, "Token should not be None"
    return {"Authorization": f"Bearer {token}"}