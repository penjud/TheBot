# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE_URI = os.getenv("DATABASE_URL")
if not DATABASE_URI:
    raise ValueError("No DATABASE_URL found in the environment variables. Please ensure it is set in your .env file.")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Base class for declarative classes
Base = declarative_base()
