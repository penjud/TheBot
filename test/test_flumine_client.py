import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from flumine_client import FlumineClient

class TestFlumineClient(unittest.TestCase):
    def setUp(self):
        # Patch the BetfairClient import to create a mock BetfairClient
        self.patcher = patch('betfair_client.BetfairClient')
        self.MockBetfairClient = self.patcher.start()
        self.mock_betfair_client_instance = self.MockBetfairClient.return_value
        
        # Initialize the FlumineClient which will use the mocked BetfairClient
        self.flumine_client = FlumineClient()

    def tearDown(self):
        self.patcher.stop()

    def test_get_betfair_client_successful(self):
        """Test successful initialization of BetfairClient."""
        self.assertIsNotNone(self.flumine_client.betfair_client)
        self.MockBetfairClient.assert_called_once()

    def test_get_betfair_client_failure(self):
        """Test failure to initialize BetfairClient."""
        self.MockBetfairClient.side_effect = Exception('Initialization error')
        flumine_client = FlumineClient()
        self.assertIsNone(flumine_client.betfair_client)
        self.MockBetfairClient.assert_called_once()

    def test_place_bet(self):
        """Test placing a bet successfully."""
        market_id = '12345'
        selection_id = '67890'
        stake = 100
        # Ensure the place_bet method on the FlumineClient calls the place_bet method on the BetfairClient
        self.flumine_client.place_bet(market_id, selection_id, stake)
        self.mock_betfair_client_instance.place_bet.assert_called_once_with(market_id, selection_id, stake)

    def test_place_bet_fail(self):
        """Test failure in placing a bet."""
        market_id = '12345'
        selection_id = '67890'
        stake = 100
        self.mock_betfair_client_instance.place_bet.side_effect = Exception('Bet placement failed')
        # Ensure the place_bet method on the FlumineClient calls the place_bet method on the BetfairClient
        self.flumine_client.place_bet(market_id, selection_id, stake)
        self.mock_betfair_client_instance.place_bet.assert_called_once_with(market_id, selection_id, stake)

    def test_get_market_book(self):
        """Test getting market book successfully."""
        market_id = '12345'
        # Ensure the get_market_book method on the FlumineClient calls the get_market_book method on the BetfairClient
        self.flumine_client.get_market_book(market_id)
        self.mock_betfair_client_instance.get_market_book.assert_called_once_with(market_id)

    def test_get_market_book_fail(self):
        """Test failure in getting market book."""
        market_id = '12345'
        self.mock_betfair_client_instance.get_market_book.side_effect = Exception('Failed to fetch market book')
        # Ensure the get_market_book method on the FlumineClient calls the get_market_book method on the BetfairClient
        result = self.flumine_client.get_market_book(market_id)
        self.assertIsNone(result)
        self.mock_betfair_client_instance.get_market_book.assert_called_once_with(market_id)

if __name__ == '__main__':
    unittest.main()
