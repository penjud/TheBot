# db_manager.py
from database.db_setup import create_tables
import logging
from database.db_queries import (
    get_upcoming_events,
    get_markets_by_event,
    get_runners_by_market,
    get_historical_data_for_runner,
    get_market_conditions,
    get_additional_data_for_runner
)
logging.basicConfig(level=logging.DEBUG)
def setup_database():
    """
    Setup the database by creating tables.

    This function orchestrates the creation of all necessary tables in the database.
    """
    create_tables()

def get_event_details():
    """
    Retrieve details for all upcoming events.

    Returns:
        List of Event objects that are scheduled to start after the current time.
    """
    return get_upcoming_events()

def get_market_details(event_id):
    """
    Retrieve all markets associated with a specific event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        List of Market objects associated with the given event.
    """
    return get_markets_by_event(event_id)

def get_runner_details(market_id):
    """
    Retrieve all runners associated with a specific market.

    Args:
        market_id (int): The ID of the market.

    Returns:
        List of Runner objects associated with the given market.
    """
    return get_runners_by_market(market_id)

def get_runner_historical_data(runner_id):
    """
    Retrieve historical data for a specific runner.

    Args:
        runner_id (int): The ID of the runner.

    Returns:
        List of HistoricalData objects associated with the given runner.
    """
    return get_historical_data_for_runner(runner_id)

def get_market_conditions_details(market_id):
    """
    Retrieve the market conditions for a specific market.

    Args:
        market_id (int): The ID of the market.

    Returns:
        The first AdditionalData object associated with the given market, or None if not found.
    """
    return get_market_conditions(market_id)

def get_runner_additional_data(runner_id):
    """
    Retrieve additional data for a specific runner.

    Args:
        runner_id (int): The ID of the runner.

    Returns:
        The first AdditionalData object associated with the given runner, or None if not found.
    """
    return get_additional_data_for_runner(runner_id)
