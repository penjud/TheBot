from sqlalchemy.orm import sessionmaker
from database.db_setup import engine, Base
from database.models import Event, Market, Runner, HistoricalData, AdditionalData
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def setup_database():
    """
    Setup the database by creating tables.

    This function orchestrates the creation of all necessary tables in the database.
    """
    Base.metadata.create_all(engine)

from datetime import datetime

def get_event_details():
    """
    Retrieve details for all upcoming events.

    Returns:
        List of Event objects that are scheduled to start after the current time.
    """
    session = Session()
    events = session.query(Event).filter(Event.start_time > datetime.now()).all()
    session.close()
    return events

def get_market_details(event_id):
    """
    Retrieve all markets associated with a specific event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        List of Market objects associated with the given event.
    """
    session = Session()
    markets = session.query(Market).filter(Market.event_id == event_id).all()
    session.close()
    return markets

def get_runner_details(market_id):
    """
    Retrieve all runners associated with a specific market.

    Args:
        market_id (int): The ID of the market.

    Returns:
        List of Runner objects associated with the given market.
    """
    session = Session()
    runners = session.query(Runner).filter(Runner.market_id == market_id).all()
    session.close()
    return runners

def get_runner_historical_data(runner_id):
    """
    Retrieve historical data for a specific runner.

    Args:
        runner_id (int): The ID of the runner.

    Returns:
        List of HistoricalData objects associated with the given runner.
    """
    session = Session()
    historical_data = session.query(HistoricalData).filter(HistoricalData.runner_id == runner_id).all()
    session.close()
    return historical_data

def get_market_conditions_details(market_id):
    """
    Retrieve the market conditions for a specific market.

    Args:
        market_id (int): The ID of the market.

    Returns:
        The first AdditionalData object associated with the given market, or None if not found.
    """
    session = Session()
    market_conditions = session.query(AdditionalData).filter(AdditionalData.market_id == market_id).first()
    session.close()
    return market_conditions

def get_runner_additional_data(runner_id):
    """
    Retrieve additional data for a specific runner.

    Args:
        runner_id (int): The ID of the runner.

    Returns:
        The first AdditionalData object associated with the given runner, or None if not found.
    """
    session = Session()
    runner_additional_data = session.query(AdditionalData).filter(AdditionalData.runner_id == runner_id).first()
    session.close()
    return runner_additional_data




'''
def add_new_event(event_data):
    """
    Add a new event to the database.

    Args:
        event_data (dict): A dictionary containing the event data.
    """
    session = Session()
    new_event = Event(**event_data)
    session.add(new_event)
    session.commit()
    session.close()

'''