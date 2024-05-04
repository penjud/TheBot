#strategy_assessment.py
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG to capture all levels of log messages
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("strategy_assessment.log"),  # Log to a file
                              logging.StreamHandler()])  # Log to console

# Adjust the path to include the root directory where 'betting' and 'database' directories are located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from betting.betting_operations import calculate_stake, place_bet
from database.db_queries import get_historical_data_for_runner, get_market_conditions, get_additional_data_for_runner
from flumine.markets.market import Market
from betfairlightweight.resources import MarketBook

class StrategyAssessment:
    def __init__(self, betfair_client):
        self.betfair_client = betfair_client
        logging.info("StrategyAssessment instance created.")

    def assess_strategies(self, market_catalogue):
        results = []
        for market in market_catalogue:
            market_id = market["marketId"]
            logging.debug(f"Processing market: {market_id}")
            market_book = self.betfair_client.betting.list_market_book(market_ids=[market_id], price_projection=["EX_BEST_OFFERS"])
            market_book = market_book[0]

            for runner in market_book.runners:
                runner_id = runner.selection_id
                logging.debug(f"Assessing runner: {runner_id}")

                historical_data = get_historical_data_for_runner(runner_id)
                market_data = get_market_conditions(market_id)
                additional_data = get_additional_data_for_runner(runner_id)

                form_score = self.assess_form(historical_data) if historical_data else 0
                price_score = self.assess_price_movements(market_id, runner_id)
                market_score = self.assess_market_conditions(market_data) if market_data else 0
                additional_score = self.assess_additional_criteria(additional_data) if additional_data else 0

                strategy_score = form_score + price_score + market_score + additional_score
                runner.strategy_score = strategy_score
                logging.info(f"Runner {runner_id} scored {strategy_score}")

            best_runner = max(market_book.runners, key=lambda x: x.strategy_score)
            result = {
                "market_id": market_id,
                "selection_id": best_runner.selection_id,
                "strategy_score": best_runner.strategy_score
            }
            results.append(result)
            logging.info(f"Best runner for market {market_id}: {best_runner.selection_id} with score {best_runner.strategy_score}")
        return results

    def assess_form(self, historical_data):
        form_score = 0
        recent_races = historical_data[-3:]  # Consider the last 3 races
        for race in recent_races:
            if race["position"] == 1:
                form_score += 20
            elif race["position"] <= 3:
                form_score += 10
            elif race["position"] <= 5:
                form_score += 5
        return form_score

    def assess_price_movements(self, market_id, runner_id):
        price_score = 0
        price_data = self.betfair_client.betting.list_runner_book(market_id=market_id, selection_id=runner_id, price_projection=["EX_BEST_OFFERS"])
        if price_data:
            price_data = price_data[0]
            if price_data.last_price_traded:
                current_price = price_data.last_price_traded
                if current_price < price_data.ex.available_to_back[0].price * 0.9:
                    price_score += 15
                elif current_price < price_data.ex.available_to_back[0].price * 0.95:
                    price_score += 10
                elif current_price > price_data.ex.available_to_lay[0].price * 1.05:
                    price_score -= 10
        return price_score

    def assess_market_conditions(self, market_data):
        market_score = 0
        if market_data["inplay"]:
            market_score -= 10
        if market_data["total_matched"] > 500000:
            market_score += 15
        elif market_data["total_matched"] > 250000:
            market_score += 10
        elif market_data["total_matched"] > 100000:
            market_score += 5
        return market_score

    def assess_additional_criteria(self, additional_data):
        additional_score = 0
        if additional_data["weather"] == "Clear":
            additional_score += 10
        if additional_data["track_condition"] in ["Good", "Good to Firm"]:
            additional_score += 10
        if additional_data["runner_weight"] < 56:  # Assuming weight is in kg
            additional_score += 5
        return additional_score
