import betfairlightweight
import logging

class BetfairClient:
    def __init__(self, username, password, app_key, certs_dir):
        self.username = username
        self.password = password
        self.app_key = app_key
        self.certs_dir = certs_dir
        self.client = None

    def login(self):
        try:
            self.client = betfairlightweight.APIClient(
                self.username,
                self.password,
                self.app_key,
                self.certs_dir
            )
            self.client.login()
            return True
        except betfairlightweight.exceptions.APIError as e:
            logging.error(f"Failed to log in: {e}")
            return False

    def keep_alive(self):
        try:
            self.client.keep_alive()
            return True
        except betfairlightweight.exceptions.APIError as e:
            logging.error(f"Failed to keep session alive: {e}")
            return False