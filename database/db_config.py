# db_config.py
import psycopg2
import os
from dotenv import load_dotenv

print("Script is starting...")

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE = os.getenv("DB_NAME", "default_database_name")
USER = os.getenv("DB_USER", "default_user")
PASSWORD = os.getenv("DB_PASSWORD", "default_password")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    """Establish a connection to the database using environment variables."""
    print("Attempting to connect to the database...")
    try:
        conn = psycopg2.connect(
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        print("Database connection established.")
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Failed to connect to database: {e}")
        return None

def create_tables():
    """Create tables in the PostgreSQL database using predefined SQL commands."""
    commands = [
        # Your SQL commands here
    ]
    
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            for command in commands:
                print(f"Attempting to execute command:\n{command}")
                cursor.execute(command)
                print("Successfully executed.")
            conn.commit()
            print("Changes have been committed to the database.")
        except psycopg2.DatabaseError as error:
            print(f"Failed to execute SQL command: {error}")
        finally:
            cursor.close()
            conn.close()
            print("Database connection closed.")
    else:
        print("Failed to establish database connection.")

def test_db_connection():
    """
    Test the database connection by attempting to connect and execute a simple query.

    Raises:
        Exception: If the connection fails or the test query fails.
    """
    conn = get_db_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute('SELECT 1')
            if cur.fetchone():
                print("Database connection successful.")
            cur.close()
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")
        finally:
            conn.close()
    else:
        raise Exception("Failed to establish database connection.")

if __name__ == "__main__":
    test_db_connection()
    create_tables()
    print("Script completed.")
