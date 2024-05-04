#!/bin/bash

echo "Starting PostgreSQL..."
# Assuming PostgreSQL is installed and configured to start automatically
# If not, you might need to start it manually. The command can vary depending on your OS.
# For example, on Ubuntu, you can use:
sudo service postgresql start

echo "Activating Python virtual environment..."
source /home/penjud/vscode_projects/place/TheBot/venv/bin/activate

echo "Setting PYTHONPATH..."
export PYTHONPATH="/home/penjud/vscode_projects/place/TheBot:$PYTHONPATH"

echo "Starting Flask server..."
cd /home/penjud/vscode_projects/place/TheBot
flask run & # Run Flask in the background

echo "Waiting for Flask server to start..."
sleep 5 # Wait for Flask to start

echo "Checking bot status..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/status)

if [ "$response" -eq 200 ]; then
    echo "Bot is already running."
else
    echo "Starting the bot via Flask API..."
    curl -X POST http://localhost:5000/start-bot
fi

echo "All components have been started."

echo "Press Enter to stop the bot and exit..."
read # Wait for user input

# Stop the bot
curl -X POST http://localhost:5000/stop-bot

echo "Bot stopped. Exiting..."