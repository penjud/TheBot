#bf_model_strat.py
import os
import pandas as pd
import logging
from dotenv import load_dotenv
from flumine import Flumine, clients, BaseStrategy
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder
from flumine.markets.market import Market
from ..betfair_client import APIClient

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Betfair API client with environment variables
username = os.getenv('BETFAIR_USERNAME')
password = os.getenv('BETFAIR_PASSWORD')
app_key = os.getenv('BETFAIR_APP_KEY')
certs = os.getenv('BETFAIR_CERT_PATH')
trading = APIClient(username, password, app_key=app_key, certs=certs)
client = clients.BetfairClient(trading)
framework = Flumine(client=client)

def download_and_prepare_model_data():
    """Function to download and prepare model data."""
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    horse_model_url = f'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/kash-ratings-model/datasets?date={today}&presenter=RatingsPresenter&csv=true'
    greyhound_model_url = f'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/iggy-joey/datasets?date={today}&presenter=RatingsPresenter&csv=true'

    # Efficient handling with Pandas for large data
    horse_data = pd.read_csv(horse_model_url)
    greyhound_data = pd.read_csv(greyhound_model_url)
    horse_data = horse_data[['market_id', 'selection_id', 'rating']].set_index(['market_id', 'selection_id'])
    greyhound_data = greyhound_data[['market_id', 'selection_id', 'rating']].set_index(['market_id', 'selection_id'])
    return horse_data, greyhound_data

horse_ratings, greyhound_ratings = download_and_prepare_model_data()

class BetfairModelStrategy(BaseStrategy):
    """Strategy class for executing bets based on model data."""
    def __init__(self, model_data, name):
        super().__init__(name=name)
        self.model_data = model_data

    def check_market_book(self, market: Market, market_book):
        return market_book.status != "CLOSED" and market.seconds_to_start < 60 and not market_book.inplay

    def process_market_book(self, market: Market, market_book):
        for runner in market_book.runners:
            if runner.status == "ACTIVE":
                try:
                    model_price = self.model_data.loc[(market_book.market_id, runner.selection_id)]['rating']
                    self.place_bets(market, runner, model_price)
                except KeyError:
                    logging.info(f"No model price available for runner {runner.selection_id} in market {market_book.market_id}")

    def place_bets(self, market, runner, model_price):
        """Places bets based on model price comparison."""
        back_price = runner.ex.available_to_back[0]['price']
        lay_price = runner.ex.available_to_lay[0]['price']
        if back_price > model_price:
            self.place_order(market, runner, back_price, "BACK", 5)
        if lay_price < model_price:
            self.place_order(market, runner, lay_price, "LAY", 5)

    def place_order(self, market, runner, price, side, size):
        trade = Trade(market_id=market.market_id, selection_id=runner.selection_id, strategy=self)
        order = trade.create_order(side=side, order_type=LimitOrder(price=price, size=size))
        market.place_order(order)
        logging.info(f"Order placed: {side} {size}@{price} on {runner.selection_id} in {market.market_id}")

# Example usage of the strategy
if __name__ == "__main__":
    horse_strategy = BetfairModelStrategy(horse_ratings, "FlatKashModel")
    greyhound_strategy = BetfairModelStrategy(greyhound_ratings, "FlatIggyModel")
    framework.add_strategy(horse_strategy)
    framework.add_strategy(greyhound_strategy)
    framework.run()
