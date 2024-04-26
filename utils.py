# utils.py
import requests
import logging
import json

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def make_api_request(url, headers, method='GET', payload=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=payload)
        logging.debug(f"API Request to {url} completed successfully.")
        return response
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def validate_response(response):
    if response and response.status_code == 200:
        return True
    else:
        logging.error(f"API call failed with status {response.status_code}: {response.text if response else 'No response body'}")
        return False

def parse_json_response(response):
    try:
        data = json.loads(response.text)
        return data
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return None
