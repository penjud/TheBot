# download_betfair_data.py

import requests

def authenticate_betfair(api_key, username, password):
    login_url = "https://identitysso-cert.betfair.com/api/certlogin"
    cert_files = ('/path/to/your/client-2048.crt', '/path/to/your/client-2048.key')  # Update with your cert paths

    headers = {
        'X-Application': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    auth_data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(login_url, data=auth_data, headers=headers, cert=cert_files)
    
    if response.status_code == 200:
        return response.json()['sessionToken']
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

# Replace with your actual credentials and file paths
session_token = authenticate_betfair('your_api_key', 'your_username', 'your_password')

def download_historical_data_file(session_token, from_date, to_date, file_type, market_types, data_path):
    data_url = "https://historicdata.betfair.com/api/DownloadListOfFiles"

    headers = {
        'X-Authentication': session_token,
        'Content-Type': 'application/json'
    }
    
    params = {
        "sport": "Horse Racing",
        "plan": "Basic Plan",
        "fromDay": from_date,
        "toDay": to_date,
        "marketTypesCollection": market_types,
        "countriesCollection": ["GB"],
        "fileTypeCollection": [file_type]
    }
    
    response = requests.get(data_url, headers=headers, params=params)
    
    if response.status_code == 200:
        with open(data_path, 'wb') as file:
            file.write(response.content)
        print(f"Data saved to {data_path}")
    else:
        raise Exception(f"Data download failed: {response.status_code} - {response.text}")

# Example usage
download_historical_data_file(
    session_token=session_token,
    from_date="2016-03-01",
    to_date="2016-03-31",
    file_type="M",  # M for Market Data
    market_types=["WIN"],  # Market Types you're interested in
    data_path="/path/to/save/march_2016_horse_racing_data.zip"  # Update with your desired save location
)
