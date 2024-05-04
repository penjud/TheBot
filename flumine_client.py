#flumine_client
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FlumineClient:
    def __init__(self):
        self.betfair_client = self.get_betfair_client()

    def get_betfair_client(self):
        try:
            from betfair_client import BetfairClient
            return BetfairClient()
        except Exception as e:
            logger.error(f"Failed to initialize Betfair client: {e}")
            return None

    def place_bet(self, market_id, selection_id, stake):
        """
        Place a bet on a given runner within a market.
        
        :param market_id: str, the unique identifier for the market
        :param selection_id: str, the unique identifier for the runner within the market
        :param stake: float, the amount of money to stake on the bet
        """
        try:
            if not self.betfair_client:
                raise ValueError("Betfair client not initialized")

            order = {
                'selectionId': selection_id,
                'stake': stake,
                'price': self.get_current_price(market_id, selection_id),  # Assuming a method to fetch current price
                'side': 'BACK'  # Assuming the default bet is to back the runner
            }
            result = self.betfair_client.place_order(market_id, order)
            logging.info(f"Bet successfully placed: {result}")
            return result
        except Exception as e:
            logging.error(f"Failed to place bet: {e}")
            return None

    def get_market_book(self, market_id):
        """
        Retrieve the market book for a given market.
        
        :param market_id: str, the unique identifier for the market
        """
        try:
            if not self.betfair_client:
                raise ValueError("Betfair client not initialized")

            market_book = self.betfair_client.get_market_book(market_id)
            logging.info(f"Market book retrieved: {market_book}")
            return market_book
        except Exception as e:
            logging.error(f"Failed to get market book: {e}")
            return None

    def get_current_price(self, market_id, selection_id):
        """
        Fetch the current price for a given runner in a market.
        
        This is a helper method used by place_bet to fetch the latest price.
        """
        market_book = self.get_market_book(market_id)
        if market_book and 'runners' in market_book:
            for runner in market_book['runners']:
                if runner['selectionId'] == selection_id:
                    return runner['latestPriceTraded']
        raise ValueError("Price for the selection not found")

# Example use within the module
if __name__ == "__main__":
    flumine = FlumineClient()
    market_id = '1.23456'  # Example market ID
    selection_id = '11223344'  # Example selection ID
    stake = 100.0  # Example stake amount
    flumine.place_bet(market_id, selection_id, stake)