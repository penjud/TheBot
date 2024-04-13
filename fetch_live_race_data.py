import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from betfair_client import BetfairClient

def get_today_racing_data():
    """Fetch today's horse racing data from Betfair API."""
    client = BetfairClient()
    url = "https://api.betfair.com/exchange/betting/rest/v1.0/listMarketCatalogue/"
    # Get today's date and format it for the API request
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime('%Y-%m-%dT00:00:00Z')
    tomorrow_str = tomorrow.strftime('%Y-%m-%dT00:00:00Z')

    # Setup the request data
    request_body = json.dumps({
        "filter": {
            "eventTypeIds": ["7"], # Horse Racing
            "marketCountries": ["AU"], # Change as needed
            "marketTypeCodes": ["WIN"], # 'WIN' markets
            "marketStartTime": {
                "from": today_str,
                "to": tomorrow_str
            }
        },
        "sort": "FIRST_TO_START",
        "maxResults": "100",
        "marketProjection": ["RUNNER_DESCRIPTION", "EVENT", "MARKET_START_TIME"]
    })

    headers = {
        'X-Application': client.app_key,
        'X-Authentication': client.session_token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, data=request_body, headers=headers)
        response.raise_for_status() # Raises a HTTPError if the response status code is 4xx or 5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")

def main():
    try:
        race_data = get_today_racing_data()
        print(json.dumps(race_data, indent=4))
    except Exception as e:
        print(f"Failed to fetch data: {e}")

if __name__ == '__main__':
    main()
