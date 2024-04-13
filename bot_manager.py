import os
import threading
import logging
from betfair_client import BetfairClient
from flumine_client import FlumineClient
from strategy_assessment import assess_strategies
from betting_bot import place_bet

class BotManager:
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        self.betfair_client = BetfairClient()
        self.flumine_client = FlumineClient()

    def start_bot(self):
        if not self.is_running:
            self.is_running = True
            self.bot_thread = threading.Thread(target=self._run_bot)
            self.bot_thread.start()
            logging.info("Bot started successfully")
            return True
        else:
            logging.info("Bot is already running.")
            return True

    def stop_bot(self):
        if self.is_running:
            self.is_running = False
            if self.bot_thread:
                self.bot_thread.join()
                self.bot_thread = None
            return True
        else:
            return False

    def _run_bot(self):
        while self.is_running:
            try:
                best_runner = assess_strategies(self.betfair_client)
                if best_runner:
                    logging.info(f"Best runner: {best_runner}")
                    place_bet(self.flumine_client, best_runner)
                else:
                    logging.info("No suitable runner found")
                self.betfair_client.keep_alive()
                # Add any additional bot logic here
            except Exception as e:
                logging.error(f"Error in bot logic: {e}")
                self.is_running = False
