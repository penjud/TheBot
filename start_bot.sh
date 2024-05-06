#!/bin/bash

VENV_PATH="/home/tim/vscode_projects/place/TheBot/venv"
REQUIREMENTS_PATH="/home/tim/VScode_Projects/place/TheBot/requirements.txt"

echo "Starting PostgreSQL..."
sudo service postgresql start
if [ $? -ne 0 ]; then
    echo -e "\e[31mFailed to start PostgreSQL\e[0m"
    exit 1
fi

if [ ! -d "$VENV_PATH" ]; then
    echo -e "\e[31mVirtual environment not found at $VENV_PATH. Please create it.\e[0m"
    exit 1
fi

echo "Activating Python virtual environment..."
source "$VENV_PATH/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "\e[31mFailed to activate Python virtual environment\e[0m"
    exit 1
fi

echo "Installing requirements..."
pip install -r "$REQUIREMENTS_PATH" || {
    echo -e "\e[33mFailed to install some requirements. Continuing with available packages...\e[0m"
}

echo "Setting PYTHONPATH..."
export PYTHONPATH="/home/tim/VScode_Projects/place/TheBot:$PYTHONPATH"

echo "Starting Flask server..."
cd /home/tim/vscode_projects/place/TheBot
export FLASK_APP=server.py
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
