import pytest
from src.database import SessionLocal
from src import models
from src.hash import hash_password
from src.pass_auth import create_access_token, verify_access_token

@pytest.fixture
def sample_user():
    return {
        'first_name': 'Sample', 
        'last_name': 'User', 
        'email': 'sampleuser@gmail.com', 
        'password': 'testpassword'
    }


@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.query(models.Messages).delete()
        db.query(models.Chats).delete()
        db.query(models.Chunks).delete()
        db.query(models.Documents).delete()
        db.query(models.Users).delete()
        db.commit()
        db.close()

    
@pytest.fixture
def db_user(db):
    db_user = {
        'first_name': 'DB', 
        'last_name': 'User', 
        'email': 'dbuser@gmail.com', 
        'password': 'testpassword'
    }

    db_user = models.Users(first_name=db_user['first_name'].strip().capitalize(), last_name=db_user['last_name'].strip().capitalize(), email=db_user['email'], password=hash_password(db_user['password']))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@pytest.fixture
def db_user_chat(db, db_user):
    db_user_chat = models.Chats(user_id = db_user.id)

    db.add(db_user_chat)
    db.commit()
    db.refresh(db_user_chat)

    return db_user_chat


@pytest.fixture
def db_user_auth(db_user):
    access_token = create_access_token(db_user.id)
    payload = verify_access_token(access_token)

    return payload