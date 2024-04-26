import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, filename='download_data.log', format='%(asctime)s - %(levelname)s - %(message)s')

def download_file_list(sport, plan, from_date, to_date, market_types, countries, file_types, session_token):
    url = 'https://historicdata.betfair.com/api/DownloadListOfFiles'
    headers = {
        'content-type': 'application/json',
        'ssoid': session_token
    }
    data = json.dumps({
        "sport": sport,
        "plan": plan,
        "fromDay": from_date.day,
        "fromMonth": from_date.month,
        "fromYear": from_date.year,
        "toDay": to_date.day,
        "toMonth": to_date.month,
        "toYear": to_date.year,
        "marketTypesCollection": market_types,
        "countriesCollection": countries,
        "fileTypeCollection": file_types
    })
    
    response = requests.post(url, headers=headers, data=data)
    logging.debug(f"Request sent to {url} with headers {headers} and payload {data}")
    logging.debug(f"Response received: {response.text}")

    if response.status_code == 200:
        try:
            file_paths = response.json()
            return file_paths
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON from response.")
            return None
    else:
        logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None

# Sample usage
session_token = "YOUR_TOKEN_HERE"
file_paths = download_file_list("Horse Racing", "Pro Plan", datetime(2015, 5, 1), datetime(2015, 5, 31),
                                ["WIN", "PLACE"], ["GB", "IE"], ["M"], session_token)
if file_paths:
    print(file_paths)
