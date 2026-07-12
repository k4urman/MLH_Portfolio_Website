#!/bin/bash

PROJECT_DIR="/root/MLH_Portfolio_Website"

echo "Starting redeployment process..."

echo "Navigating to project folder: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Directory not found!"; exit 1; }

echo "Fetching latest changes from GitHub..."
git fetch && git reset origin/main --hard

echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate
pip install -r requirements.txt

echo "Restarting the portfolio system service..."
sudo systemctl restart myportfolio

echo "Redeployment completed successfully via systemd service!"
