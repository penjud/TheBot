# bot_manager.py

from flumine_client import FlumineClient
from betfair_client import BetfairClient
from strategy.strategy_manager import StrategyManager
from betting.betting_bot import BettingBot
from database.db_factory import create_db # Adjust the import path as necessary
import threading
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_setup import load_environment, create_database_engine

# Load environment variables and create database engine
database_uri = load_environment()
engine = create_database_engine(database_uri)
Session = sessionmaker(bind=engine)

def init_bot():
    # Create session at the start of the bot
    session = Session()
    # Your bot's initialization code here
    print("Bot initialized with database session")
    return session
logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
class BotManager:
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        self.session = None # Add a session attribute to the class
        
        try:
            logging.info("Initializing Betfair client...")
            self.betfair_client = BetfairClient()
            logging.info("Betfair client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Betfair client: {e}")
            raise

        try:
            logging.info("Initializing Flumine client...")
            self.flumine_client = FlumineClient()
            logging.info("Flumine client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Flumine client: {e}")
            raise

        try:
            logging.info("Initializing Strategy Manager...")
            self.strategy_manager = StrategyManager(self.betfair_client)
            logging.info("Strategy Manager initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Strategy Manager: {e}")
            raise

        try:
            logging.info("Initializing Betting Bot...")
            self.betting_bot = BettingBot(self.flumine_client)
            logging.info("Betting Bot initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Betting Bot: {e}")
            raise

        try:
            logging.info("Setting up database...")
            self.session = create_db() # Initialize the session here
            logging.info("Database setup completed successfully.")
        except Exception as e:
            logging.error(f"Failed to set up database: {e}")
            raise

    def start_bot(self):
        if not self.is_running:
            try:
                logging.info("Attempting to start the bot...")
                self.bot_thread = threading.Thread(target=self._run_bot)
                self.bot_thread.start()
                logging.info("Bot thread started.")
                try:
                    self.bot_thread.join(timeout=5) # Wait for 5 seconds to check if the thread starts properly
                    if self.bot_thread.is_alive():
                        self.is_running = True
                        logging.info("Bot started successfully")
                        return True
                    else:
                        logging.error("Bot failed to start properly.")
                        return False
                except Exception as e:
                    logging.error(f"Error waiting for bot thread to start: {e}")
                    return False
            except Exception as e:
                logging.error(f"Error starting the bot: {e}")
                return False
        else:
            logging.info("Bot is already running.")
            return False

    def stop_bot(self):
        if self.is_running:
            logging.info("Attempting to stop the bot...")
            self.is_running = False
            if self.bot_thread:
                self.bot_thread.join() # Ensure the thread finishes cleanly
                self.bot_thread = None
            logging.info("Bot stopped successfully")
            return True
        else:
            logging.info("Bot is not running.")
            return False

    def _run_bot(self):
        try:
            logging.info("Initializing bot components...")
            # Initialize the Betfair client for API connections
            self.betfair_client = BetfairClient()
            
            # Initialize the Flumine client for placing bets
            self.flumine_client = FlumineClient()
            
            # Initialize the strategy manager with the Betfair client
            self.strategy_manager = StrategyManager(self.betfair_client)
            
            # Initialize the betting bot with the Flumine client
            self.betting_bot = BettingBot(self.flumine_client)
            
            # Set up the database
            self.session = create_db() # Ensure the session is initialized here

            logging.info("Bot components initialized successfully.")

            while self.is_running:
                try:
                    # Retrieve the market catalogue using the strategy manager
                    logging.info("Retrieving market catalogue...")
                    market_catalogue = self.strategy_manager.get_market_catalogue()
                    
                    # Retrieve the best runner using the strategy manager and the market catalogue
                    logging.info("Retrieving best runner...")
                    best_runner = self.strategy_manager.get_best_runner(market_catalogue)
                    
                    if best_runner:
                        logging.info(f"Best runner: {best_runner}")
                        logging.info("Placing bet on best runner...")
                        self.betting_bot.place_bet(best_runner)
                    else:
                        logging.info("No suitable runner found")
                    
                    # Additional logic can be added here
                except Exception as e:
                    logging.error(f"Error in bot logic: {e}")
                    self.is_running = False
        except Exception as e:
            logging.error(f"Error initializing bot components: {e}")
            self.is_running = False
if __name__ == "__main__":
    session = init_bot()
    # Example of bot's lifecycle handling
    try:
        # Bot operations here
        print("Bot is running...")
    finally:
        session.close()  # Ensure session is closed when done