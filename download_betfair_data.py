# download_betfair_data.py

import os
import requests
import urllib.parse
import logging
from dotenv import load_dotenv
import json
from betfair_client import BetfairClient

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

class AuthenticationException(Exception):
    """Custom exception class for authentication failures."""
    pass

def check_certificates():
    cert_path = os.path.join(os.getenv('BETFAIR_CERT_PATH'))
    if not os.path.exists(cert_path):
        raise FileNotFoundError(f"Certificate path {cert_path} does not exist.")
    
    cert_files = (
        os.path.join(cert_path, 'client-2048.crt'),
        os.path.join(cert_path, 'client-2048.key')
    )
    for cert_file in cert_files:
        if not os.path.exists(cert_file):
            raise FileNotFoundError(f"Certificate file {cert_file} does not exist.")
    
    return cert_files

def authenticate_betfair():
    try:
        betfair_client = BetfairClient()
        session_token = betfair_client.get_session_token()
        if session_token:
            return session_token
        else:
            raise AuthenticationException("Authentication failed: No session token returned")
    except Exception as e:
        logging.error('Authentication failed: %s', e)
        raise AuthenticationException("Authentication failed") from e

def download_historical_data_file(session_token, from_date, to_date, file_type, market_types, data_path):
    data_url = "https://historicdata.betfair.com/api/DownloadListOfFiles"
    headers = {
        'X-Authentication': session_token,
        'Content-Type': 'application/json'
    }
    params = {
        "sport": "Horse Racing",
        "plan": "Pro Plan",
        "fromDay": from_date,
        "toDay": to_date,
        "marketTypesCollection": market_types,
        "countriesCollection": ["GB"],
        "fileTypeCollection": [file_type]
    }
    try:
        response = requests.get(data_url, headers=headers, params=params)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content: {response.content}")
        
        response.raise_for_status()
        
        if response.content.startswith(b'{'):
            save_data_to_file(response.content, data_path)
        else:
            logging.error("Invalid response content. Expected JSON data.")
            raise DataDownloadException("Invalid response content")
    except requests.RequestException as e:
        logging.error(f"Data download failed: {e}")
        raise DataDownloadException("Failed to download data") from e

def save_data_to_file(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(data)
    logging.info("Data saved to %s", path)

class DataDownloadException(Exception):
    pass

def main():
    try:
        market_types_str = os.getenv('MARKET_TYPES')
        if market_types_str is None:
            raise ValueError("Environment variable 'MARKET_TYPES' is not set")
        try:
            market_types = json.loads(market_types_str)
        except json.JSONDecodeError:
            raise ValueError("Environment variable 'MARKET_TYPES' does not contain valid JSON")

        session_token = authenticate_betfair()
        print('Session Token:', session_token)
        download_historical_data_file(
            session_token=session_token,
            from_date=os.getenv('FROM_DATE'),
            to_date=os.getenv('TO_DATE'),
            file_type=os.getenv('FILE_TYPE'),
            market_types=market_types,
            data_path=os.getenv('DOWNLOADS_PATH')
        )
    except Exception as e:
        logging.error('Error during operation: %s', e)

if __name__ == '__main__':
    main()
