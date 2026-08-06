from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import VECTOR
from .database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Chats(Base):
    __tablename__ = 'chats'
    
    id = Column(Integer, primary_key=True)
    chat_title = Column(String, default='New Chat')
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    role = Column(String)
    message_text = Column(Text)
    chat_id = Column(Integer, ForeignKey('chats.id'), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    document_name = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    # ADD A FILE TYPE COLUMN FOR WHEN MORE FILE TYPES ARE IMPLEMENTED
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class Chunks(Base):
    __tablename__ = 'chunks'

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), index=True)
    chunk_id = Column(String, unique=True)
    chunk_text = Column(Text)
    embedding = Column(VECTOR(1536))
    created_at = Column(DateTime(timezone=True), server_default=func.now())