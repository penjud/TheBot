# db_config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE_URI = os.getenv("DATABASE_URL")
if not DATABASE_URI:
    raise ValueError("No DATABASE_URL found in the environment variables.")

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def create_all_tables():
    """Create all tables defined in the Base metadata."""
    print("Creating all tables in the database...")
    Base.metadata.create_all(engine)
    print("All tables created successfully.")

def test_db_connection():
    """Test the database connection using SQLAlchemy engine."""
    try:
        conn = engine.connect()
        print("Testing database connection...")
        conn.execute('SELECT 1')
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_db_connection()
    create_all_tables()
    print("Script completed.")
# The db_config.py script provides functions to create all tables in the database and test the database connection.