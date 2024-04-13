echo "Stopping the bot via Flask API..."
curl -X POST http://localhost:5000/stop
echo "Bot has been stopped."