# db_connection.py
import psycopg2
from db_config import get_db_connection_params

def get_db_connection():
    params = get_db_connection_params()
    conn = psycopg2.connect(**params)
    return conn
