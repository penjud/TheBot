# test_strategies.py
from TheBot.strategy.strategy_assessment_tester import StrategyAssessment
from betfair_client import BetfairClient
from database.db_queries import get_historical_data, get_simulated_market_data

def test_strategy_assessment():
    betfair_client = BetfairClient()
    strategy_assessment = StrategyAssessment(betfair_client)

    # Retrieve historical data for testing
    historical_data = get_historical_data()

    # Simulate market data for testing
    simulated_market_data = get_simulated_market_data()

    # Test the strategy assessment logic
    for market_data in simulated_market_data:
        market_catalogue = market_data["market_catalogue"]
        results = strategy_assessment.assess_strategies(market_catalogue)

        # Analyze the results and compare against historical outcomes
        for result in results:
            market_id = result["market_id"]
            selection_id = result["selection_id"]
            strategy_score = result["strategy_score"]

            # Retrieve the actual outcome from historical data
            actual_outcome = get_actual_outcome(historical_data, market_id, selection_id)

            # Compare the strategy score with the actual outcome
            if strategy_score > 50 and actual_outcome == "WIN":
                print(f"Market {market_id}, Selection {selection_id}: Correct prediction (WIN)")
            elif strategy_score <= 50 and actual_outcome == "LOSE":
                print(f"Market {market_id}, Selection {selection_id}: Correct prediction (LOSE)")
            else:
                print(f"Market {market_id}, Selection {selection_id}: Incorrect prediction")

def get_actual_outcome(historical_data, market_id, selection_id):
    # Retrieve the actual outcome from historical data
    # Return "WIN" if the selection won, "LOSE" otherwise
    # Implement the logic based on the structure of your historical data
    pass

if __name__ == "__main__":
    test_strategy_assessment()