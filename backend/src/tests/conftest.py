import pytest
from src.database import SessionLocal

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_user():
    return {'first_name': 'Test', 'last_name': 'User', 'email': 'testuser@gmail.com', 'password': 'testpassword'}

