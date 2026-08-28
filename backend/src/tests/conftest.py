import pytest
from src.database import SessionLocal
from src import models
from src.hash import hash_password

@pytest.fixture
def sample_user():
    return {
        'first_name': 'Test', 
        'last_name': 'User', 
        'email': 'testuser@gmail.com', 
        'password': 'testpassword'
    }


@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@pytest.fixture
def db_user(db):
    db_user = {
        'first_name': 'Test', 
        'last_name': 'User', 
        'email': 'testuser@gmail.com', 
        'password': 'testpassword'
    }

    db_user = models.Users(first_name=db_user['first_name'].strip().capitalize(), last_name=db_user['last_name'].strip().capitalize(), email=db_user['email'], password=hash_password(db_user['password']))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
