from flask import Flask, jsonify, Response
from bot_manager import BotManager
from typing import Tuple

app = Flask(__name__)
bot_manager = BotManager()

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Returns a JSON response with the status 'success'.
    """
    return jsonify({'status': 'success'})

@app.route('/start', methods=["POST"])
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
        return jsonify({"message": "Failed to start the bot"}), 503

@app.route('/stop', methods=["POST"])

def stop_bot_endpoint() -> Tuple[Response, int]:
    if bot_manager.stop_bot():
        return jsonify({"message": "Bot stopped successfully"}), 200
    else:
        return jsonify({"message": "Bot is not running"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)