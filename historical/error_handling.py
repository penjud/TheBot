# error_handling.py
import logging

logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)

def log_error(message):
    logging.error(message)
