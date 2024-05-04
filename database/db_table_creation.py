# db_table_creation.py
from database.db_connection import get_db_connection

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS market (
            ...
        )
        """,
        # Add other table creation SQL commands
    )
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
