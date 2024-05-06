# download_betfair_data.py

import os
import bz2
import logging
import requests
from betfair_client import BetfairClient
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataDownloadException(Exception):
    """Custom exception for data download failures."""
    pass

def download_historical_data_files(session_token, file_list):
    """
    Downloads historical data files from Betfair.

    :param session_token: The session token for authentication.
    :param file_list: A list of file paths to download.
    """
    for file_info in file_list:
        file_path = file_info
        file_name = os.path.basename(file_path)
        data_url = "https://historicdata.betfair.com/api/DownloadFile"
        headers = {'ssoid': session_token}
        params = {'filePath': file_path}
    try:
        response = requests.get(data_url, headers=headers, params=params, timeout=60)
        response.raise_for_status()  # to trigger an HTTPError for bad responses
        logging.debug("Data successfully retrieved.")
        save_path = os.path.join('Data', 'downloads', file_name)
        save_data_to_file(response.content, save_path)
        extract_bz2_file(save_path, os.path.join('Data', 'historical_data'))
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve data: {str(e)}")
        raise SystemExit(e)  # Stop execution and exit

    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

def get_file_list(session_token, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year,
                 event_id=None, event_name=None, market_types_collection=None, countries_collection=None,
                 file_type_collection=None):
    """
    Retrieves a list of files available for download from Betfair.

    :param session_token: The session token for authentication.
    :param sport: The sport to filter files by.
    :param plan: The plan to filter files by.
    :param from_day: The start day for the file range.
    :param from_month: The start month for the file range.
    :param from_year: The start year for the file range.
    :param to_day: The end day for the file range.
    :param to_month: The end month for the file range.
    :param to_year: The end year for the file range.
    :param event_id: Optional event ID to filter files by.
    :param event_name: Optional event name to filter files by.
    :param market_types_collection: Optional collection of market types to filter files by.
    :param countries_collection: Optional collection of countries to filter files by.
    :param file_type_collection: Optional collection of file types to filter files by.
    :return: A list of file paths available for download.
    """
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
        response = requests.get(data_url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve file list: {e}")
        raise DataDownloadException("Failed to retrieve file list") from e

def save_data_to_file(data, path):
    """
    Saves data to a file.

    :param data: The data to save.
    :param path: The path to save the data to.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(data)
    logging.info(f"Data saved to {path}")

def extract_bz2_file(bz2_path, extract_path):
    """
    Extracts a BZ2 file to a specified path.

    :param bz2_path: The path to the BZ2 file.
    :param extract_path: The path to extract the file to.
    """
    with bz2.BZ2File(bz2_path, 'rb') as bz2_file:
        file_name = os.path.basename(bz2_path).replace('.bz2', '')
        extract_file_path = os.path.join(extract_path, file_name)
        with open(extract_file_path, 'wb') as output_file:
            output_file.write(bz2_file.read())
    logging.info(f"BZ2 file extracted to {extract_file_path}")

def main():
    """
    Main entry point for downloading Betfair historical data.
    """

    server_url = "https://historicdata.betfair.com"  # Adjust to a URL that you know should be reachable
    try:
        response = requests.head(server_url, timeout=10)
        response.raise_for_status()  # Check for usual HTTP errors
        logging.debug("Server is reachable.")
    except requests.RequestException as e:
        logging.error("Server is not reachable. Check your network or server URL.")
        raise SystemExit(e)  # Stop execution if the server is not reachable

    try:
        betfair_client = BetfairClient()
        betfair_client.login()
        session_token = betfair_client.get_session_token()
        
        sport = "Horse Racing"
        plan = "Pro Plan"
        from_day = "01"
        from_month = "07"
        from_year = "2015"
        to_day = "10"
        to_month = "07"
        to_year = "2015"
        
        file_list = get_file_list(session_token, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year)
        logging.info(f"File list: {file_list}")
        download_historical_data_files(session_token, file_list)
        
    except Exception as e:
        logging.error(f"Error during operation: {e}")

# Example of logging around file operations
file_path = "/home/tim/VScode_Projects/place/TheBot/Data/historical_data"  # Replace "path/to/file" with the actual file path
logging.debug(f"Saving data to {file_path}")
try:
    data = b'some data'
    with open(file_path, 'wb') as file:
        file.write(data)
    logging.debug(f"Data saved successfully to {file_path}")
except IOError as e:
    logging.error(f"Failed to save data to {file_path}: {str(e)}")
    raise SystemExit(e)  # Stop execution and exit

if __name__ == '__main__':
    main()
