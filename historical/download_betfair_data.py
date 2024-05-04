# download_betfair_data.py

import os
import requests
import logging
import bz2
from betfair_client import BetfairClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataDownloadException(Exception):
    pass

def download_historical_data_files(session_token, file_list):
    for file_info in file_list:
        file_path = file_info  # Directly use the file path string
        file_name = os.path.basename(file_path)
        data_url = f"https://historicdata.betfair.com/api/DownloadFile"
        headers = {'ssoid': session_token}
        params = {'filePath': file_path}
        
        try:
            response = requests.get(data_url, headers=headers, params=params)
            response.raise_for_status()
            logging.info(f"Downloaded file: {file_name}")
            save_path = os.path.join('Data', 'downloads', file_name)
            save_data_to_file(response.content, save_path)
            extract_bz2_file(save_path, os.path.join('Data', 'historical_data'))
        except requests.exceptions.RequestException as e:
            logging.error(f"Data download failed for file {file_name}: {e}")
            raise DataDownloadException(f"Failed to download data for file {file_name}") from e

def get_file_list(session_token, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year,
                  event_id=None, event_name=None, market_types_collection=None, countries_collection=None,
                  file_type_collection=None):
    data_url = "https://historicdata.betfair.com/api/DownloadListOfFiles"
    headers = {'ssoid': session_token}
    params = {
        'sport': sport,
        'plan': plan,
        'fromDay': from_day,
        'fromMonth': from_month,
        'fromYear': from_year,
        'toDay': to_day,
        'toMonth': to_month,
        'toYear': to_year,
        'eventId': event_id,
        'eventName': event_name,
        'marketTypesCollection': market_types_collection,
        'countriesCollection': countries_collection,
        'fileTypeCollection': file_type_collection
    }
    
    try:
        response = requests.get(data_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve file list: {e}")
        raise DataDownloadException("Failed to retrieve file list") from e

def save_data_to_file(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(data)
    logging.info(f"Data saved to {path}")

def extract_bz2_file(bz2_path, extract_path):
    with bz2.BZ2File(bz2_path, 'rb') as bz2_file:
        file_name = os.path.basename(bz2_path).replace('.bz2', '')
        extract_file_path = os.path.join(extract_path, file_name)
        with open(extract_file_path, 'wb') as output_file:
            output_file.write(bz2_file.read())
    logging.info(f"BZ2 file extracted to {extract_file_path}")

def main():
    try:
        betfair_client = BetfairClient()
        betfair_client.login()
        session_token = betfair_client.get_session_token()
        
        sport = "Horse Racing"
        plan = "Pro Plan"
        from_day = "01"
        from_month = "03"
        from_year = "2016"
        to_day = "30"
        to_month = "03"
        to_year = "2016"
        
        file_list = get_file_list(session_token, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year)
        print(f"File list: {file_list}")
        download_historical_data_files(session_token, file_list)
        
    except Exception as e:
        logging.error(f"Error during operation: {e}")

if __name__ == '__main__':
    main()