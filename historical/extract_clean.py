import json
import bz2
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Replace 'your_dsn' with your actual PostgreSQL DSN connection string
dsn = "your_dsn"

# Function to connect to the PostgreSQL database
def connect_to_db(dsn):
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

# Function to create the table
def create_table(cursor):
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS runner_data (
            market_id VARCHAR(50),
            runner_id INTEGER,
            last_traded_price NUMERIC,
            total_matched NUMERIC,
            status VARCHAR(20),
            adjustment_factor NUMERIC
        )
    """)
    cursor.execute(create_table_query)

# Function to extract and clean data from the file
def extract_and_clean_data(file_path):
    cleaned_data = []
    with bz2.open(file_path, 'rt') as file:  # Opening as 'rt' to read as text
        for line in file:
            try:
                json_data = json.loads(line)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for line: {line}")
                continue
            
            # Example of extraction, modify as per your JSON structure and requirements
            for market in json_data.get('mc', []):  # Assuming 'mc' contains market changes
                market_id = market.get('id')
                for runner in market.get('rc', []):  # Assuming 'rc' contains runner changes
                    runner_id = runner.get('id')
                    last_traded_price = runner.get('ltp')
                    total_matched = runner.get('tv')
                    status = runner.get('status')
                    adjustment_factor = runner.get('at')

                    # Append a tuple of the data to the cleaned_data list
                    cleaned_data.append((market_id, runner_id, last_traded_price, total_matched, status, adjustment_factor))

    return cleaned_data

# Function to insert data into the database
def insert_data(cursor, cleaned_data):
    insert_query = sql.SQL("""
        INSERT INTO runner_data (market_id, runner_id, last_traded_price, total_matched, status, adjustment_factor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """)
    cursor.executemany(insert_query, cleaned_data)

def main():
    # Replace 'path_to_your_data' with the actual path to the extracted data file
    file_path = '/home/penjud/vscode_projects/place/TheBot/Data'
    cleaned_data = extract_and_clean_data(file_path)
    
    # Database operations
    conn = connect_to_db(dsn)
    cursor = conn.cursor()
    create_table(cursor)
    insert_data(cursor, cleaned_data)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

