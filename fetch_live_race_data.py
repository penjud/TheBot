import os
import requests
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from betfair_client import BetfairClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_today_racing_data():
    """Fetch today's horse racing data from Betfair API."""
    try:
        client = BetfairClient()
        client.login()
        client.start_keep_alive() # Ensure the session is kept alive

        method = 'SportsAPING/v1.0/listMarketCatalogue'
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        today_str = today.strftime('%Y-%m-%dT00:00:00Z')
        tomorrow_str = tomorrow.strftime('%Y-%m-%dT00:00:00Z')

        params = {
            "filter": {
                "eventTypeIds": ["7"], # Horse Racing
                "marketCountries": ["AU"], # Change as needed
                "marketTypeCodes": ["WIN"], # 'WIN' markets
                "marketStartTime": {"from": today_str, "to": tomorrow_str}
            },
            "sort": "FIRST_TO_START",
            "maxResults": "100",
            "marketProjection": ["RUNNER_DESCRIPTION", "EVENT", "MARKET_START_TIME"]
        }

        response = client.api_request(method, params)
        return response
    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        raise

def main():
    try:
        race_data = get_today_racing_data()
        # Directly print the race_data without using json.dumps, as it's already a JSON-serializable object
        print(race_data)
    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")

if __name__ == '__main__':
    main()
