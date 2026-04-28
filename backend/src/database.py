from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL_DATABASE = os.getenv('DB_URL')

# Handle DB connection
engine = create_engine(URL_DATABASE)

# Handle sessions per DB request
SessionLocal = sessionmaker(bind=engine)

# Handle table definitions/metadata
Base = declarative_base()