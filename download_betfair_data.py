# download_betfair_data.py

import os
import requests
import logging
import zipfile
from betfair_client import BetfairClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataDownloadException(Exception):
    pass

def download_historical_data_file(session_token, file_list):
    for file_info in file_list:
        file_id = file_info['id']
        file_name = file_info['name']
        data_url = f"https://historicdata.betfair.com/api/v1/file/{file_id}"
        headers = {
            'ssoid': session_token
        }
        try:
            response = requests.get(data_url, headers=headers)
            response.raise_for_status()
            logging.info(f"Downloaded file: {file_name}")
            save_path = os.path.join('Data', 'downloads', file_name)
            save_data_to_file(response.content, save_path)
            extract_zip_file(save_path, os.path.join('Data', 'historical_data'))
        except requests.exceptions.RequestException as e:
            logging.error(f"Data download failed for file {file_name}: {e}")
            raise DataDownloadException(f"Failed to download data for file {file_name}") from e

def get_file_list(session_token, sport_id):
    data_url = "https://historicdata.betfair.com/api/v1/getfilelist"
    headers = {
        'ssoid': session_token,
        'content-type': 'application/json'
    }
    data = {
        'sport': sport_id,
        'plan': 'Pro Plan'
    }
    try:
        response = requests.post(data_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['fileList']
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve file list: {e}")
        raise DataDownloadException("Failed to retrieve file list") from e

def save_data_to_file(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(data)
    logging.info(f"Data saved to {path}")

def extract_zip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    logging.info(f"ZIP file extracted to {extract_path}")

def main():
    try:
        betfair_client = BetfairClient()
        betfair_client.login()
        session_token = betfair_client.get_session_token()
        
        sport_id = '7'  # Horse Racing
        
        file_list = get_file_list(session_token, sport_id)
        download_historical_data_file(session_token, file_list)
        
    except Exception as e:
        logging.error(f"Error during operation: {e}")

if __name__ == '__main__':
    main()