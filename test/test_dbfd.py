import unittest
from unittest.mock import patch, MagicMock
from betfair_client import BetfairClient

class TestBetfairClient(unittest.TestCase):

    @patch('betfair_client.requests.post')
    def setUp(self, mock_post):
        # Mock the response from the Betfair API for login
        mock_response = MagicMock()
        mock_response.json.return_value = {'sessionToken': 'mock_session_token'}
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()  # No exception for success status
        mock_post.return_value = mock_response

        # Initialize the BetfairClient with mock data
        self.client = BetfairClient(
            username='mock_username',
            password='mock_password',
            app_key='mock_app_key',
            cert_path='mock_cert_path'
        )
    @patch('betfair_client.requests.post')
    def test_login(self, mock_post):
        # Mock the response from the Betfair API
        mock_response = MagicMock()
        mock_response.json.return_value = {'sessionToken': 'mock_session_token'}
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()  # No exception for success status
        mock_post.return_value = mock_response

        # Initialize the BetfairClient with mock data
        client = BetfairClient(
            username='mock_username',
            password='mock_password',
            app_key='mock_app_key',
            cert_path='mock_cert_path'
        )

        # Assert that the login method returns the expected session token
        self.assertEqual(client.session_token, 'mock_session_token')

    @patch('betfair_client.requests.post')
    def test_api_request(self, mock_post):
        # Mock the response from the Betfair API
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': {'status': 'SUCCESS'}}
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()  # No exception for success status
        mock_post.return_value = mock_response

        # Initialize the BetfairClient with mock data
        client = BetfairClient(
            username='mock_username',
            password='mock_password',
            app_key='mock_app_key',
            cert_path='mock_cert_path'
        )

        # Call the api_request method with mock data
        endpoint = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        payload = {
            'jsonrpc': '2.0',
            'method': 'SportsAPING/v1.0/listEvents',
            'params': {'filter': {'eventTypeIds': ['1']}},
            'id': 1
        }
        response = client.api_request(endpoint, payload)

        # Assert that the api_request method returns the expected response
        self.assertEqual(response, {'result': {'status': 'SUCCESS'}})

if __name__ == '__main__':
    unittest.main()
