echo "Starting PostgreSQL..."
# Add commands to start PostgreSQL if needed

echo "Activating Python virtual environment..."
source /home/penjud/vscode_projects/place/TheBot/venv/bin/activate

echo "Setting PYTHONPATH..."
export PYTHONPATH="/home/penjud/vscode_projects/place/TheBot:$PYTHONPATH"

echo "Starting Flask server..."
cd /home/penjud/vscode_projects/place/TheBot
flask run

echo "Starting the bot via Flask API..."
# Ensure Flask server is up before making requests
sleep 5
curl http://localhost:5000/start-bot

echo "All components have been started."



