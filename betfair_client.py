import os
import requests
import threading
import time
from dotenv import load_dotenv

class BetfairClient:
    def __init__(self, username=None, password=None, app_key=None, cert_path=None):
        load_dotenv()
        self.username = username or os.getenv('BETFAIR_USERNAME')
        self.password = password or os.getenv('BETFAIR_PASSWORD')
        self.app_key = app_key or os.getenv('BETFAIR_APP_KEY')
        self.cert_path = cert_path or os.getenv('BETFAIR_CERT_PATH')
        self.cert_files = (f"{self.cert_path}/client-2048.crt", f"{self.cert_path}/client-2048.key")
        self.session_token = self.login() # Store session token on login
        self.keep_alive_thread = None

    def login(self):
        """Log in to Betfair API using certificates and retrieve the session token."""
        login_url = 'https://identitysso-cert.betfair.com/api/certlogin'
        headers = {'X-Application': self.app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': self.username, 'password': self.password}
        response = requests.post(login_url, data=data, headers=headers, cert=self.cert_files)
        if response.status_code == 200 and 'sessionToken' in response.json():
            return response.json()['sessionToken']
        else:
            error_msg = response.json().get('error', 'No error message available')
            raise Exception(f"Failed to log in: {response.status_code} - {error_msg}")

    def api_request(self, endpoint, payload):
        """Make an authenticated API request and handle session token expiration."""
        headers = {
            'X-Authentication': self.session_token,
            'X-Application': self.app_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif 'error' in response.json() and 'INVALID_SESSION_INFORMATION' in response.text:
            print("Session token invalid, attempting to re-login.")
            self.session_token = self.login() # Refresh the token
            return self.api_request(endpoint, payload) # Retry the request with a new session token
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

    def keep_alive(self):
        """Periodically refresh the session token to prevent expiration."""
        while True:
            try:
                # Assuming there's an endpoint to keep the session alive, replace with actual endpoint
                keep_alive_endpoint = 'https://api.betfair.com/exchange/keepalive/json-rpc/v1'
                payload = {'jsonrpc': '2.0', 'method': 'SessionAPING/v1.0/keepAlive', 'params': {}, 'id': 1}
                self.api_request(keep_alive_endpoint, payload)
                print("Session kept alive.")
            except Exception as e:
                print(f"Failed to keep the session alive: {e}")
            time.sleep(60) # Wait for 60 seconds before the next keep-alive request

    def start_keep_alive(self):
        """Start the keep_alive thread."""
        if self.keep_alive_thread is None:
            self.keep_alive_thread = threading.Thread(target=self.keep_alive)
            self.keep_alive_thread.start()

# Example usage
if __name__ == "__main__":
    client = BetfairClient()
    client.start_keep_alive() # Start the keep_alive thread
    endpoint = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
    payload = {'jsonrpc': '2.0', 'method': 'SportsAPING/v1.0/listEvents', 'params': {}, 'id': 1}
    try:
        response = client.api_request(endpoint, payload)
        print(response)
    except Exception as e:
        print(f"Error occurred: {e}")

