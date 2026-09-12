import pytest
from src.database import SessionLocal
from src import models
from src.hash import hash_password
from src.pass_auth import create_access_token, verify_access_token
import io
from fpdf import FPDF

@pytest.fixture
def sample_user():
    return {
        'first_name': 'Sample', 
        'last_name': 'User', 
        'email': 'sampleuser@gmail.com', 
        'password': 'testpassword'
    }


@pytest.fixture
def sample_pdf_file():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=11)
    pdf.cell(text='This is a sample pdf file for testing purposes.')

    return ('sample.pdf', io.BytesIO(pdf.output()), 'application/pdf')


@pytest.fixture
def sample_pdf_file_path(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=11)
    pdf.cell(text='This is a sample pdf file for testing purposes.')

    pdf_path = tmp_path / 'sample.pdf'
    pdf.output(str(pdf_path))

    return pdf_path


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
def db_user_auth(db_user):
    access_token = create_access_token(db_user.id)
    payload = verify_access_token(access_token)

    return payload


@pytest.fixture
def db_user_chat(db, db_user_auth):
    db_user_chat = models.Chats(chat_title='Test Chat', user_id=db_user_auth['sub'])

    db.add(db_user_chat)
    db.commit()
    db.refresh(db_user_chat)

    return db_user_chat


@pytest.fixture
def db_user_chat_messages(db, db_user_chat):
    db_user_message = models.Messages(role='user', message_text='This is an example prompt', chat_id=db_user_chat.id)
    db_assistant_message = models.Messages(role='assistant', message_text='This is an example bot response', chat_id=db_user_chat.id)

    db.add(db_user_message)
    db.add(db_assistant_message)
    db.commit()

    return [db_user_message, db_assistant_message]


@pytest.fixture
def db_user_document(db, db_user_auth):
    db_user_document = models.Documents(document_name='Test Chat', user_id=db_user_auth['sub'], s3_key=None, file_type='pdf')

    db.add(db_user_document)
    db.commit()
    db.refresh(db_user_document)

    return db_user_document