#strategy_assessment_historical.py
import os
import logging
from dotenv import load_dotenv
from TheBot.strategy.strategy_assessment_tester import StrategyAssessment
# strategy_assessment_historical.py

from ..database.db_queries import get_historical_data_for_runner, get_market_conditions, get_additional_data_for_runner
from betfair_client import BetfairClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

try:
    # Initialize the Betfair client with environment variables
    betfair_client = BetfairClient(username=os.environ.get("BETFAIR_USERNAME"), password=os.environ.get("BETFAIR_PASSWORD"))

    # Fetch historical data from the database
    historical_data = get_historical_data_for_strategy_assessment()

    # Create an instance of StrategyAssessment
    strategy_assessment = StrategyAssessment(betfair_client)

    # Assess strategies using historical data
    results = strategy_assessment.assess_strategies(historical_data)

    # Process the results and store them in the database
    for result in results:
        market_id = result["market_id"]
        selection_id = result["selection_id"]
        strategy_score = result["strategy_score"]
        logging.info(f"Market {market_id}: Best selection {selection_id} with score {strategy_score}")
        store_strategy_assessment_results(market_id, selection_id, strategy_score)

except Exception as e:
    logging.error(f"An error occurred: {e}")
