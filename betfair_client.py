#betfair_client.py
import os
import requests
import threading
import time
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

class BetfairClient:
    def __init__(self, username=None, password=None, app_key=None, cert_path=None):
        load_dotenv() 
        print(os.getenv('BETFAIR_USERNAME'))
        print(os.getenv('BETFAIR_PASSWORD'))
        print(os.getenv('BETFAIR_APP_KEY'))
        print(os.getenv('BETFAIR_CERT_PATH'))
 # Ensure environment variables are loaded
        self.username = username or os.getenv('BETFAIR_USERNAME')
        self.password = password or os.getenv('BETFAIR_PASSWORD')
        self.app_key = app_key or os.getenv('BETFAIR_APP_KEY')
        self.cert_path = cert_path or os.getenv('BETFAIR_CERT_PATH')
        self.cert_files = (f"{self.cert_path}/client-2048.crt", f"{self.cert_path}/client-2048.key")
        
        # Log the certificate paths to ensure they are correctly loaded
        logging.debug(f"Certificate CRT file: {self.cert_files[0]}")
        logging.debug(f"Certificate KEY file: {self.cert_files[1]}")

        try:
            self.session_token = self.login()  # Login and store session token
        except Exception as e:
            logging.error("Failed to authenticate with Betfair API.", exc_info=True)
            raise

        self.keep_alive_thread = None

    def login(self):
        """Login to Betfair API using certificates and retrieve the session token."""
        login_url = 'https://identitysso-cert.betfair.com/api/certlogin'
        headers = {'X-Application': self.app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': self.username, 'password': self.password}
        
        logging.debug("Attempting to login to Betfair API.")
        response = requests.post(login_url, data=data, headers=headers, cert=self.cert_files)
        
        try:
            response.raise_for_status()
            response_json = response.json()
            logging.debug("Authentication successful.")
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP error occurred during login.", exc_info=True)
            raise
        except ValueError as e:
            logging.error("Invalid JSON response received.", exc_info=True)
            raise

        session_token = response_json.get('sessionToken')
        if session_token:
            return session_token
        else:
            error_msg = response_json.get('loginStatus', 'Unknown error')
            raise Exception(f"Failed to retrieve session token. Login status: {error_msg}")

    # Additional methods with logging...

    def api_request(self, endpoint, payload):
        """Send requests to the Betfair API using the correct session token and headers."""
        headers = {
            'X-Application': self.app_key,
            'X-Authentication': self.session_token,
            'Content-Type': 'application/json'
        }
        logging.debug(f"Sending API request to {endpoint}")
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def start_keep_alive(self):
        """Start the keep_alive thread to run continuously in the background."""
        if self.keep_alive_thread is None:
            self.keep_alive_thread = threading.Thread(target=self.keep_alive, daemon=True)
            self.keep_alive_thread.start()

    def keep_alive(self):
        """Periodically refresh the session token to prevent expiration."""
        keep_alive_endpoint = 'https://api.betfair.com/exchange/keepalive/json-rpc/v1'
        payload = {
            'jsonrpc': '2.0',
            'method': 'SessionAPING/v1.0/keepAlive',
            'params': {},
            'id': 1
        }
        while True:
            try:
                response = self.api_request(keep_alive_endpoint, payload)
                if response.get('result', {}).get('status') != 'SUCCESS':
                    logging.error(f"Keep alive failed: {response}")
                else:
                    logging.info("Session kept alive successfully.")
            except Exception as e:
                logging.error(f"Error during keep alive: {e}")
            time.sleep(60)  # Wait for 60 seconds before the next keep-alive request

    def retrieve_market_catalogue(self, market_filter):
        """Retrieve market catalogue from Betfair API."""
        endpoint = 'https://api.betfair.com/exchange/betting/rest/v1.0/listMarketCatalogue/'
        payload = {
            'filter': market_filter,
            'maxResults': '1000',
            'marketProjection': ['EVENT', 'EVENT_TYPE', 'COMPETITION', 'RUNNER_DESCRIPTION', 'MARKET_START_TIME']
        }
        try:
            response = self.api_request(endpoint, payload)
            return response
        except Exception as e:
            logging.error(f"Failed to retrieve market catalogue: {e}")
            logging.error(f"API request parameters: {market_filter}")
            logging.error(f"API endpoint: {endpoint}")
            logging.error(f"Session token: {self.session_token}")
            return []
        
    def get_market_conditions(self, market_id):
        """Retrieve market conditions for a given market ID."""
        market_catalogue = self.betting_client.list_market_catalogue(
            filter={'marketIds': [market_id]},
            market_projection=['RUNNER_DESCRIPTION', 'MARKET_LIQUIDITY']
        )
        return market_catalogue
    
    def get_session_token(self):
        """Return the current session token."""
        return self.session_token

# Example usage
if __name__ == "__main__":
    client = BetfairClient()
    client.start_keep_alive()
    market_filter = {'eventTypeIds': ['1']} # Example filter for retrieving specific events
    try:
        market_catalogue = client.retrieve_market_catalogue(market_filter)
        print(market_catalogue)
    except Exception as e:
        print(f"Error retrieving market catalogue: {e}")
