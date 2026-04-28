from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)


class Chats(Base):
    __tablename__ = 'chats'
    
    id = Column(Integer, primary_key=True, index=True)
    # ChatList 
    chat = Column(String, index=True) # TEST
    #user_id = Column(Integer, ForeignKey('users.id'))