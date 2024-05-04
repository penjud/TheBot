
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from betfair_client import BetfairClient
def test_api_request():
    # Initialize the client once and use it for making the API request
    client = BetfairClient(username="penjud", password="_W3r3w0lf70", app_key="mECg2P2ohk92MLXy", cert_path="certs")
    endpoint = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
    # Setting up a simple filter for demonstration, you can customize it as per your requirements
    filter_params = {
        'eventTypeIds': ['1'],  # Sample event type ID for horse racing, replace or extend as needed
        'marketCountries': ['GB']  # Filter markets to a specific country, here 'GB' for Great Britain
    }
    payload = {
        'jsonrpc': '2.0', 
        'method': 'SportsAPING/v1.0/listEvents', 
        'params': {
            'filter': filter_params,  
            'maxResults': 1  # Adjust the number of results as needed
        }, 
        'id': 1
    }
    try:
        response = client.api_request(endpoint, payload)
        print("Response:", response)
    except Exception as e:
        print(f"Error occurred: {e}")

def test_login():
    # Initialize the client once and use it for logging in
    client = BetfairClient(username="penjud", password="_W3r3w0lf70", app_key="mECg2P2ohk92MLXy", cert_path="certs")
    try:
        session_token = client.login()
        print("Session Token:", session_token)
    except Exception as e:
        print(f"Error occurred during login: {e}")

if __name__ == "__main__":
    # Call the functions to test them
    test_login()  # Ensures that login is working as expected
    test_api_request()  # Tests the API request functionality
