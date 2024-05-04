# db_queries.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to the database:", error)
        return None

def get_historical_data_for_runner(runner_id):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_data WHERE runner_id = %s", (runner_id,))
        historical_data = cur.fetchall()
        cur.close()
        conn.close()
        return historical_data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching historical data for runner:", error)
        return None

def get_market_conditions(market_id):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM market_conditions WHERE market_id = %s", (market_id,))
        market_conditions = cur.fetchone()
        cur.close()
        conn.close()
        return market_conditions
    except (Exception, psycopg2.Error) as error:
        print("Error fetching market conditions:", error)
        return None

def get_additional_data_for_runner(runner_id):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM additional_data WHERE runner_id = %s", (runner_id,))
        additional_data = cur.fetchone()
        cur.close()
        conn.close()
        return additional_data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching additional data for runner:", error)
        return None

def get_historical_data():
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_data")
        historical_data = cur.fetchall()
        cur.close()
        conn.close()
        return historical_data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching historical data:", error)
        return None

def get_simulated_market_data():
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM simulated_market_data")
        simulated_market_data = cur.fetchall()
        cur.close()
        conn.close()
        return simulated_market_data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching simulated market data:", error)
        return None
    
def get_upcoming_events():
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM upcoming_events") # Adjust the query as needed
        upcoming_events = cur.fetchall()
        cur.close()
        conn.close()
        return upcoming_events # This line ensures that upcoming_events is returned and used.
    except (Exception, psycopg2.Error) as error:
        print("Error fetching upcoming events:", error)
        return None
    
def get_runners_by_market(market_id):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM runners WHERE market_id = %s", (market_id,))
        runners = cur.fetchall()
        cur.close()
        conn.close()
        return runners
    except (Exception, psycopg2.Error) as error:
        print("Error fetching runners by market:", error)
        return None
def get_markets_by_event(event_id):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM markets WHERE event_id = %s", (event_id,))
        markets = cur.fetchall()
        cur.close()
        conn.close()
        return markets
    except (Exception, psycopg2.Error) as error:
        print("Error fetching markets by event:", error)
        return None