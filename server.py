import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from bot_manager import BotManager

load_dotenv()

app = Flask(__name__)
bot_manager = BotManager()

@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({'status': 'success'})

@app.route('/start', methods=["POST"])
def start_bot_endpoint():
    if bot_manager.start_bot():
        return jsonify({"message": "Bot started successfully"}), 200
    else:
        return jsonify({"message": "Failed to start the bot"}), 500

@app.route('/stop', methods=["POST"])
def stop_bot_endpoint():
    if bot_manager.stop_bot():
        return jsonify({"message": "Bot stopped successfully"}), 200
    else:
        return jsonify({"message": "Bot is not running"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)