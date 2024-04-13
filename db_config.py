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
    
    """Create tables in the PostgreSQL database with correct dependency order and foreign keys."""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS sports (
            sport_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id SERIAL PRIMARY KEY,
            sport_id INTEGER REFERENCES sports(sport_id),
            name VARCHAR(255) NOT NULL,
            start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            venue VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS markets (
            market_id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES events(event_id),
            market_name VARCHAR(255) NOT NULL,
            market_type VARCHAR(255) NOT NULL,
            market_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            market_status VARCHAR(50) NOT NULL,
            number_of_winners INTEGER,
            number_of_active_runners INTEGER,
            bet_delay INTEGER,
            bsp_reconciled BOOLEAN,
            complete BOOLEAN,
            in_play BOOLEAN,
            cross_matching BOOLEAN,
            runners_voidable BOOLEAN,
            turn_in_play_enabled BOOLEAN,
            version INTEGER
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS runners (
            runner_id SERIAL PRIMARY KEY,
            market_id INTEGER REFERENCES markets(market_id),
            selection_id INTEGER,
            runner_name VARCHAR(255) NOT NULL,
            handicap DOUBLE PRECISION,
            status VARCHAR(50) NOT NULL,
            sort_priority INTEGER,
            last_traded_price DOUBLE PRECISION,
            total_matched DOUBLE PRECISION,
            adjustment_factor DOUBLE PRECISION,
            removal_date TIMESTAMP WITHOUT TIME ZONE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            api_key VARCHAR(255),
            session_token VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bets (
            bet_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            runner_id INTEGER REFERENCES runners(runner_id),
            stake DECIMAL(18, 2) NOT NULL,
            price DECIMAL(18, 2) NOT NULL,
            placed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            outcome VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS market_changes (
            change_id SERIAL PRIMARY KEY,
            market_id INTEGER REFERENCES markets(market_id),
            published_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            change_type VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS price_volume_data (
            data_id SERIAL PRIMARY KEY,
            runner_id INTEGER REFERENCES runners(runner_id),
            market_id INTEGER REFERENCES markets(market_id),
            price DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            time_recorded TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS historical_data (
            historical_id SERIAL PRIMARY KEY,
            market_id INTEGER REFERENCES markets(market_id),
            event_id INTEGER REFERENCES events(event_id),
            data TEXT NOT NULL,
            captured_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS additional_data (
            additional_data_id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES events(event_id),
            data_type VARCHAR(255) NOT NULL,
            value TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS betfair_api_usage (
            usage_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            api_key VARCHAR(255),
            operation VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        """,

            """
            CREATE TABLE IF NOT EXISTS runners (
                runner_id SERIAL PRIMARY KEY,
                market_id INTEGER REFERENCES markets(market_id),
                selection_id INTEGER,
                runner_name VARCHAR(255) NOT NULL,
                handicap DOUBLE PRECISION,
                status VARCHAR(50) NOT NULL,
                sort_priority INTEGER,
                last_traded_price DOUBLE PRECISION,
                total_matched DOUBLE PRECISION,
                adjustment_factor DOUBLE PRECISION,
                removal_date TIMESTAMP WITHOUT TIME ZONE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                api_key VARCHAR(255),
                session_token VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bets (
                bet_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                runner_id INTEGER REFERENCES runners(runner_id),
                stake DECIMAL(18, 2) NOT NULL,
                price DECIMAL(18, 2) NOT NULL,
                placed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                outcome VARCHAR(50)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS market_changes (
                change_id SERIAL PRIMARY KEY,
                market_id INTEGER REFERENCES markets(market_id),
                published_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                change_type VARCHAR(50) NOT NULL
            );
            """,
        """
        CREATE TABLE IF NOT EXISTS price_volume_data (
            data_id SERIAL PRIMARY KEY,
            runner_id INTEGER REFERENCES runners(runner_id),
            market_id INTEGER REFERENCES markets(market_id),
            price DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            time_recorded TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        """,
        """
            CREATE TABLE IF NOT EXISTS historical_data (
                historical_id SERIAL PRIMARY KEY,
                market_id INTEGER REFERENCES markets(market_id),
                event_id INTEGER REFERENCES events(event_id),
                data TEXT NOT NULL,
                captured_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS additional_data (
                additional_data_id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES events(event_id),
                data_type VARCHAR(255) NOT NULL,
                value TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS betfair_api_usage (
                usage_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                api_key VARCHAR(255),
                operation VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
            );
            """,
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

if __name__ == "__main__":
    create_tables()
    print("Script completed.")
