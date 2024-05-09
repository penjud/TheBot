# strategy_assessment_historical.py
from ..database.db_queries import get_historical_data_for_runner, get_market_conditions, get_additional_data_for_runner

class StrategyAssessmentHistorical:
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def assess_strategies(self):
        assessed_data = []
        for market_id, market_data in self.historical_data.items():
            for runner_id, runner_data in market_data["runners"].items():
                historical_data = get_historical_data_for_runner(runner_id)
                market_conditions = get_market_conditions(market_id)
                additional_data = get_additional_data_for_runner(runner_id)

                form_score = self.assess_form(historical_data)
                price_score = self.assess_price_movements(runner_data)
                market_score = self.assess_market_conditions(market_conditions)
                additional_score = self.assess_additional_criteria(additional_data)

                strategy_score = form_score + price_score + market_score + additional_score

                assessed_data.append({
                    "market_id": market_id,
                    "runner_id": runner_id,
                    "strategy_score": strategy_score,
                    "form_score": form_score,
                    "price_score": price_score,
                    "market_score": market_score,
                    "additional_score": additional_score
                })

        return assessed_data

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

    def assess_price_movements(self, runner_data):
        price_score = 0
        if "sp" in runner_data and "price_history" in runner_data:
            sp = runner_data["sp"]
            price_history = runner_data["price_history"]
            if price_history:
                current_price = price_history[-1]
                if current_price < sp * 0.9:
                    price_score += 15
                elif current_price < sp * 0.95:
                    price_score += 10
                elif current_price > sp * 1.05:
                    price_score -= 10
        return price_score

    def assess_market_conditions(self, market_conditions):
        market_score = 0
        if market_conditions["inplay"]:
            market_score -= 10
        if market_conditions["total_matched"] > 500000:
            market_score += 15
        elif market_conditions["total_matched"] > 250000:
            market_score += 10
        elif market_conditions["total_matched"] > 100000:
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