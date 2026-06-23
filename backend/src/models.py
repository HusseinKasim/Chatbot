from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.database import Base

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