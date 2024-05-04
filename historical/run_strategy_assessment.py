from strategy.strategy_assessment import StrategyAssessment
from database.db_queries import get_historical_data_for_strategy_assessment, store_strategy_assessment_results
import os
from dotenv import load_dotenv
from betfair_client import BetfairClient

# Load environment variables from .env file
load_dotenv()

# Fetch historical data from the database
betfair_client = BetfairClient(username=os.environ.get("BETFAIR_USERNAME"), password=os.environ.get("BETFAIR_PASSWORD"))

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
    print(f"Market {market_id}: Best selection {selection_id} with score {strategy_score}")
    store_strategy_assessment_results(market_id, selection_id, strategy_score)
