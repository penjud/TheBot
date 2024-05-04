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
    
def get_historical_data_for_strategy_assessment():
    try:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("""
            SELECT
                m.market_id,
                r.runner_id,
                r.runner_name,
                hd.historical_data,
                mc.market_conditions,
                ad.additional_data
            FROM
                markets m
                JOIN runners r ON m.market_id = r.market_id
                JOIN historical_data hd ON m.market_id = hd.market_id
                JOIN market_conditions mc ON m.market_id = mc.market_id
                JOIN additional_data ad ON hd.market_id = ad.market_id  # Corrected join condition
        """)
        historical_data = cur.fetchall()
        cur.close()
        conn.close()

        # Process the data into a list of dictionaries
        processed_data = []
        for market_data in historical_data:
            market_id, runner_id, runner_name, historical_data_for_runner, market_conditions, additional_data = market_data
            market_dict = {
                "market_id": market_id,
                "runners": [
                    {
                        "runner_id": runner_id,
                        "runner_name": runner_name,
                        "historical_data": historical_data_for_runner,
                        "additional_data": additional_data
                    }
                ],
                "market_conditions": market_conditions
            }
            processed_data.append(market_dict)

        return processed_data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching historical data for strategy assessment:", error)
        return None

def store_strategy_assessment_results(market_id, selection_id, strategy_score):
    try:
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("INSERT INTO strategy_assessment_results (market_id, selection_id, strategy_score) VALUES (%s, %s, %s)", (market_id, selection_id, strategy_score))
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Error storing strategy assessment results:", error)
