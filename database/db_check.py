#db_check.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

def test_db_connection():
    """
    Test the database connection using SQLAlchemy session.
    """
    session = Session()
    try:
        # Test connection by executing a simple query
        result = session.execute('SELECT 1')
        if result.scalar():
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_db_connection()
