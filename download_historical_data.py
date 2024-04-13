import os
from dotenv import load_dotenv
import requests
from betfair_client import BetfairClient

load_dotenv()

app_key = os.getenv('BETFAIR_APP_KEY')
cert_path = os.getenv('BETFAIR_CERT_PATH')
downloads_path = os.getenv('DOWNLOADS_PATH')

# Initialize the Betfair client from your betfair_client.py
client = BetfairClient()

# Authenticate and get a session token using betfair_client.py
session_token = client.get_session_token()

# Betfair Historical Data Service API endpoint for file list download
historical_data_endpoint = "https://historicdata.betfair.com/api/DownloadListOfFiles"

# Headers for the request
headers = {
    'X-Application': app_key,
    'X-Authentication': session_token,
    'Content-Type': 'application/json'
}

# Define the location for saving the downloaded file
download_location = downloads_path

# Request payload, adjust 'marketStartTime' as needed
payload = {
    "marketStartTime": {
        "from": "2016-03-01T00:00:00Z",
        "to": "2016-03-31T23:59:59Z"
    },
    "marketTypesCollection": ["WIN"],
    "countriesCollection": ["AU"],
    "fileTypeCollection": ["M"]
}

# Perform the download request
def download_historical_data():
    # Authenticate using certificates
    cert_files = (f"{cert_path}/client-2048.crt", f"{cert_path}/client-2048.key")

    # Make the POST request
    response = requests.post(historical_data_endpoint, headers=headers, json=payload, cert=cert_files)

    # Check response status and download file if successful
    if response.status_code == 200:
        with open(f"{download_location}/historical_data.zip", 'wb') as file:
            file.write(response.content)
        print(f"Data successfully downloaded to {download_location}/historical_data.zip")
    else:
        print(f"Failed to download data: {response.status_code} - {response.reason}")

# Run the download function
if __name__ == "__main__":
    download_historical_data()
