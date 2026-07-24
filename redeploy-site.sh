#!/bin/bash

PROJECT_DIR="/root/MLH_Portfolio_Website"

echo "Starting redeployment process..."

echo "Navigating to project folder: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Directory not found!"; exit 1; }

echo "Fetching latest changes from GitHub..."
git fetch && git reset origin/main --hard

echo "Stopping containers..."
docker compose -f docker-compose.prod.yml down

echo "Building and launching updated containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Docker redepoly completed!"
