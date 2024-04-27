import os
import betfairdatabase as bfdb
from dotenv import load_dotenv
import psycopg2
from historical.db_config import get_db_connection

# Load environment variables
load_dotenv()

# Path to your Betfair data
path_to_data = "./Data/downloads/historical_data.zip"

# Index the Betfair data
bfdb.index(path_to_data)

# Example query using betfairdatabase
dataset = bfdb.select(path_to_data, where="eventTypeId='4339' AND eventVenue='Sheffield'")
for market in dataset:
    print(market["marketDataFilePath"], market["marketCatalogueFilePath"])

# Connect to your PostgreSQL database
conn = get_db_connection()

# Test the database connection
try:
    conn.isolation_level
except psycopg2.OperationalError as oe:
    print("Connection is not active. Attempting to reconnect...")
    conn = get_db_connection()

# Example of inserting data into PostgreSQL (you'll need to adapt this to your specific data structure)
cursor = conn.cursor()
# Assuming you have a table named 'betfair_data' and columns 'market_data_path', 'market_catalogue_path'
cursor.execute("INSERT INTO betfair_data (market_data_path, market_catalogue_path) VALUES (%s, %s)",
               (market["marketDataFilePath"], market["marketCatalogueFilePath"]))
conn.commit()

# Close the database connection
cursor.close()
conn.close()
