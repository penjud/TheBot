#!/bin/bash

echo "Stopping the bot via Flask API..."
curl -X POST http://localhost:5000/stop

echo "Stopping Flask server..."
# Find the process ID of the Flask server more reliably
flask_pid=$(ps aux | grep 'flask run' | grep -v grep | awk '{print $2}')

if [ -n "$flask_pid" ]; then
  echo "Killing Flask server process ID $flask_pid"
  kill -9 $flask_pid
  echo "Flask server stopped."
else
  echo "Flask server not running."
fi

# It's a good practice to ensure that the command 'deactivate' is run in the same shell where 'activate' was run
echo "Deactivating Python virtual environment..."
source /home/penjud/vscode_projects/place/TheBot/venv/bin/activate
deactivate

echo "Stopping PostgreSQL..."
sudo service postgresql stop

echo "All components have been stopped."