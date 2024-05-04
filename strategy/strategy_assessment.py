# strategy_assessment.py
from betting.betting_operations import calculate_stake, place_bet
from database.db_queries import get_historical_data_for_runner, get_market_conditions, get_additional_data_for_runner
from flumine.markets.market import Market
from betfairlightweight.resources import MarketBook

class StrategyAssessment:
    def __init__(self, betfair_client):
        self.betfair_client = betfair_client

    def assess_strategies(self, historical_data):
        if historical_data is None:
            print("No historical data available.")
            return []

        results = []
        for market_data in historical_data:
            market_id = market_data["market_id"]
            runners = market_data["runners"]

            market_book = MarketBook(market_id, runners)

            for runner in market_book.runners:
                runner_id = runner.selection_id
                historical_data_for_runner = get_historical_data_for_runner(runner_id)
                market_conditions = get_market_conditions(market_id)
                additional_data = get_additional_data_for_runner(runner_id)

                form_score = self.assess_form(historical_data_for_runner)
                price_score = self.assess_price_movements(market_id, runner_id)
                market_score = self.assess_market_conditions(market_conditions)
                additional_score = self.assess_additional_criteria(additional_data)

                strategy_score = sum([form_score, price_score, market_score, additional_score])
                runner.strategy_score = strategy_score
                results.append({
                    "market_id": market_id,
                    "selection_id": runner_id,
                    "strategy_score": strategy_score
                })

            if market_book.runners:
                best_runner = max(market_book.runners, key=lambda x: x.strategy_score)
                stake = calculate_stake(best_runner.strategy_score)
                market_object = Market(market_id)
                place_bet(self.betfair_client, market_object, best_runner.selection_id, stake)

        return results

    def assess_form(self, historical_data):
        if not historical_data:
            return 0

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
            if price_data.last_price_traded and price_data.ex.available_to_back and price_data.ex.available_to_lay:
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
        if additional_data.get("weather") == "Clear":
            additional_score += 10
        if additional_data.get("track_condition") in ["Good", "Good to Firm"]:
            additional_score += 10
        if additional_data.get("runner_weight", float('inf')) < 56:  # Assuming weight is in kg
            additional_score += 5
        return additional_score
