# server.py

from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
from bot_manager import BotManager
from typing import Tuple

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models after initializing the db object
from database.models import *

bot_manager = BotManager()

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Returns a JSON response with the status of the bot.
    """
    if bot_manager.is_running:
        return jsonify({'status': 'running'}), 200
    else:
        return jsonify({'status': 'stopped'}), 200

@app.route('/start-bot', methods=["POST"])
def start_bot_endpoint() -> Tuple[Response, int]:
    """
    Handles a POST request to start the bot.

    Returns:
        A JSON response with a success message and a status code of 200 if the bot is started successfully.
        A JSON response with an error message and a status code of 500 if the bot fails to start.
    """
    if bot_manager.start_bot():
        return jsonify({"message": "Bot started successfully"}), 200
    else:
        return jsonify({"message": "Failed to start the bot"}), 500

@app.route('/stop-bot', methods=["POST"])
def stop_bot_endpoint() -> Tuple[Response, int]:
    if bot_manager.stop_bot():
        return jsonify({"message": "Bot stopped successfully"}), 200
    else:
        return jsonify({"message": "Bot is not running"}), 200

if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
