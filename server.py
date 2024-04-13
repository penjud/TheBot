import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from bot_manager import BotManager
import threading

load_dotenv()

app = Flask(__name__)
bot_manager = BotManager()

@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({'status': 'success'})

def start_bot():
    global is_running, framework
    while is_running:
        try:
            framework.run()
        except Exception as e:
            app.logger.error(f"Error in bot logic: {e}")
            is_running = False
bot_thread = None

def stop_bot():
    global is_running, bot_thread
    global is_running
    if is_running:
        is_running = False
        if bot_thread:
            bot_thread.join()
        return True
    else:
        return False

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