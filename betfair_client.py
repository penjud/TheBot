import os
import requests
import threading
import time
from dotenv import load_dotenv
import json

class BetfairClient:
    def __init__(self, username=None, password=None, app_key=None, cert_path=None):
        load_dotenv()
        self.username = username or os.getenv('BETFAIR_USERNAME')
        self.password = password or os.getenv('BETFAIR_PASSWORD')
        self.app_key = app_key or os.getenv('BETFAIR_APP_KEY')
        self.cert_path = cert_path or os.getenv('BETFAIR_CERT_PATH')
        self.cert_files = (f"{self.cert_path}/client-2048.crt", f"{self.cert_path}/client-2048.key")
        self.session_token = self.login()  # Store session token on login
        self.keep_alive_thread = None
    def get_session_token(self):
        return self.session_token

    def login(self):
        """Log in to Betfair API using certificates and retrieve the session token."""
        login_url = 'https://identitysso-cert.betfair.com/api/certlogin'
        headers = {'X-Application': self.app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': self.username, 'password': self.password}
        response = requests.post(login_url, data=data, headers=headers, cert=self.cert_files)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        response_json = response.json()
        if 'sessionToken' in response_json:
            return response_json['sessionToken']
        else:
            error_msg = response_json.get('error', 'No error message available')
            raise Exception(f"Failed to log in: {response.status_code} - {error_msg}")

    def api_request(self, endpoint, payload):
        """Send requests to the Betfair API."""
        headers = {
            'X-Application': self.app_key, 
            'X-Authentication': self.session_token, 
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        return response.json()

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
                    print(f"Keep alive failed: {response}")
                else:
                    print("Session kept alive successfully.")
            except Exception as e:
                print(f"Error during keep alive: {e}")
            time.sleep(60)  # Wait for 60 seconds before the next keep-alive request

    def start_keep_alive(self):
        """Start the keep_alive thread to run continuously in the background."""
        if self.keep_alive_thread is None:
            self.keep_alive_thread = threading.Thread(target=self.keep_alive, daemon=True)
            self.keep_alive_thread.start()

# Example usage
if __name__ == "__main__":
    client = BetfairClient()
    client.start_keep_alive()  # Start the keep_alive thread and continue with other tasks
    endpoint = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
    payload = {
        'jsonrpc': '2.0',
        'method': 'SportsAPING/v1.0/listEvents',
        'params': {'filter': {'eventTypeIds': ['1']}},  # Example parameter
        'id': 1
    }
    try:
        response = client.api_request(endpoint, payload)
        print(response)
    except Exception as e:
        print(f"API request error: {e}")
