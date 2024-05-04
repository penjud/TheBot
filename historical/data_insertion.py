# data_insertion.py
from database.db_connection import get_db_connection
from error_handling import log_error

def insert_data(table, data):
    # Insert data into the given table
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # SQL insert statement
        cursor.executemany(...)
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log_error(f"Error inserting data: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
