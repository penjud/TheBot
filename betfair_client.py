import os
import threading
import time
import logging
from betfairlightweight import APIClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

class BetfairClient:
    def __init__(self):
        self.username = os.environ.get('BETFAIR_USERNAME')
        self.password = os.environ.get('BETFAIR_PASSWORD')
        self.app_key = os.environ.get('BETFAIR_APP_KEY')
        self.certs_path = os.environ.get('BETFAIR_CERT_PATH')
        self.session_token = None
        self.keep_alive_thread = None
        
        self.client = APIClient(
            username=self.username,
            password=self.password,
            app_key=self.app_key,
            certs=self.certs_path
        )
    
    def login(self):
        try:
            self.client.login()
            self.session_token = self.client.session_token
            logging.info(f"Logged in successfully. Session token: {self.session_token}")
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise
    
    def get_session_token(self):
        return self.session_token

    def api_request(self, method, params):
        """Send requests to the Betfair API."""
        try:
            response = self.client.betting.request(method, params, session=self.client.session)
            return response
        except Exception as e:
            logging.exception("An error occurred during API request")
            raise

    def keep_alive(self):
        """Periodically refresh the session token to prevent expiration."""
        while True:
            try:
                self.client.keep_alive()
                logging.info("Session kept alive successfully.")
            except Exception as e:
                logging.exception("Error during keep alive.")
            time.sleep(60)  # Adjust frequency as necessary

    def start_keep_alive(self):
        """Start the keep_alive thread to run continuously in the background."""
        if self.keep_alive_thread is None:
            self.keep_alive_thread = threading.Thread(target=self.keep_alive, daemon=True)
            self.keep_alive_thread.start()

# Example usage
if __name__ == "__main__":
    client = BetfairClient()
    client.login()
    client.start_keep_alive()  # Start the keep_alive thread and continue with other tasks
    method = 'SportsAPING/v1.0/listEvents'
    params = {'filter': {'eventTypeIds': ['1']}}  # Example parameter
    try:
        response = client.api_request(method, params)
        print(response)
    except Exception as e:
        print(f"API request error: {e}")