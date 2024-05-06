# db_test.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv
load_dotenv()

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Assuming DATABASE_URL is set in your environment variables, or load from .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Define the raw SQL query
# Define the raw SQL query using the text() function
sql_query = text("SELECT * FROM some_table WHERE id = :x")

# Execute the query with a parameter
with engine.connect() as connection:
    result = connection.execute(sql_query, {'x': 7})  # Replace '1' with the actual ID you want to query

    # Print the results
    for row in result:
        print(row)

try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connection OK:", result.fetchone())
except OperationalError as e:
    print("Database connection FAILED:", str(e))
    exit(1)
