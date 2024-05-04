import json
import bz2
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Function to connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(DSN)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

# Function to create the table
def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runner_data (
                market_id VARCHAR(50),
                runner_id INTEGER,
                last_traded_price NUMERIC,
                total_matched NUMERIC,
                status VARCHAR(20),
                adjustment_factor NUMERIC
            )
        """)
        print("Table created or verified successfully.")

# Function to extract and clean data from the file
def extract_and_clean_data(file_path):
    cleaned_data = []
    with bz2.open(file_path, 'rt') as file:
        for line in file:
            try:
                json_data = json.loads(line)
                # Assume 'mc' contains market changes and 'rc' contains runner changes
                for market in json_data.get('mc', []):
                    market_id = market.get('id')
                    for runner in market.get('rc', []):
                        runner_data = (
                            market_id,
                            runner.get('id'),
                            runner.get('ltp'),  # last traded price
                            runner.get('tv'),  # total matched volume
                            runner.get('status'),
                            runner.get('at')   # adjustment factor
                        )
                        cleaned_data.append(runner_data)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for line: {line}")
                continue
    print(f"Extracted and cleaned {len(cleaned_data)} records from {os.path.basename(file_path)}.")
    return cleaned_data

# Function to insert data into the database
def insert_data(conn, cleaned_data):
    with conn.cursor() as cursor:
        cursor.executemany("""
            INSERT INTO runner_data (market_id, runner_id, last_traded_price, total_matched, status, adjustment_factor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, cleaned_data)
        print(f"Inserted {cursor.rowcount} records into the database.")

def main():
    conn = None  # Initialize the connection variable to ensure it is in scope for the finally block
    try:
        conn = connect_to_db()  # Attempt to connect to the database
        print("Connected to the database successfully.")
        create_table(conn)  # Create the table if it does not already exist

        directory = '/home/penjud/vscode_projects/place/TheBot/Data/downloads/'
        files = os.listdir(directory)  # Get a list of files in the directory
        bz2_files = [f for f in files if f.endswith('.bz2')]  # Filter for .bz2 files
        if not bz2_files:
            print("No .bz2 files found in the directory.")
        for filename in bz2_files:
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {filename}")  # Log which file is being processed
            try:
                cleaned_data = extract_and_clean_data(file_path)  # Extract and clean data from the file
                if cleaned_data:
                    insert_data(conn, cleaned_data)  # Insert cleaned data into the database
                    print(f"Data from {filename} inserted successfully.")
                else:
                    print(f"No valid data found to insert for {filename}.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    except Exception as e:
        print(f"Error during database connection or table creation: {e}")
    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed
            print("Database connection closed.")


if __name__ == "__main__":
    main()
