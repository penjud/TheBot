#db_factory.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Declarative base class
Base = declarative_base()

def create_db():
    """
    Configures and returns a session factory bound to the engine.

    :return: Session factory
    """
    # Ensure all models are imported so that they are registered with the metadata
    # This is necessary for the tables to be created
    import_all_models()

    # Create all tables in the database
    Base.metadata.create_all(engine)

    return Session

def import_all_models():
    """
    Dynamically import all models to ensure they are registered with the metadata.
    This is necessary for the tables to be created.
    """
    # Import your models here
    # For example:
    # from .models import User, Post
    pass

