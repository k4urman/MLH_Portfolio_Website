#!/bin/bash

PROJECT_DIR="/root/MLH_Portfolio_Website"

echo "Starting redeployment process..."

echo "Killing existing tmux sessions..."
tmux kill-server 2>/dev/null || true

echo "Navigating to project folder: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Directory not found!"; exit 1; }

echo "Fetching latest changes from GitHub..."
git fetch --all
git reset origin/main --hard

echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate
pip install -r requirements.txt

echo "Starting Flask server inside a new detached tmux session..."
tmux new-session -d -s flask-server 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'

echo "Redeployment completed successfully!"
