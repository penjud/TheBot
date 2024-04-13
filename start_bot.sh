#!/bin/bash
echo "Starting PostgreSQL..."
sudo service postgresql start

echo "Activating Python virtual environment..."
source /home/penjud/vscode_projects/place/TheBot/venv/bin/activate

echo "Starting Flask server..."
export FLASK_APP=/home/penjud/vscode_projects/place/TheBot/server.py
flask run &

# Wait for Flask server to start
echo "Waiting for Flask server to initialize..."
sleep 5

echo "Starting the bot via Flask API..."
curl -X POST http://localhost:5000/start

echo "All components have been started."



