import unittest
from unittest.mock import patch, MagicMock
import requests
from fetch_live_race_data import get_today_racing_data

class TestFetchLiveRaceData(unittest.TestCase):
    @patch('fetch_live_race_data.BetfairClient')
    @patch('fetch_live_race_data.requests.post')
    def test_get_today_racing_data_http_error(self, mock_post, mock_BetfairClient):
        # Setup the mock BetfairClient
        mock_client = MagicMock()
        mock_client.app_key = 'fake_app_key'
        mock_client.session_token = 'fake_session_token'
        mock_BetfairClient.return_value = mock_client

        # Setup the mock to simulate an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP error simulated by unittest")
        mock_post.return_value = mock_response

        # Check if an HTTPError is raised as expected
        with self.assertRaises(requests.exceptions.HTTPError):
            get_today_racing_data()

        # Optionally, test the actual logging
        with self.assertLogs(level='ERROR') as log:
            try:
                get_today_racing_data()
            except requests.exceptions.HTTPError:
                pass
            self.assertTrue(any("HTTP error occurred" in message for message in log.output))

if __name__ == '__main__':
    unittest.main()
