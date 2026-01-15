#!/bin/bash
# Test script to run daily check with credentials from .env

# Load credentials from .env
export $(cat .env | grep -v '^#' | xargs)

# Map TELEGRAM_API_KEY to TELEGRAM_BOT_TOKEN
export TELEGRAM_BOT_TOKEN=$TELEGRAM_API_KEY

echo "Testing Daily Check Script..."
echo "=============================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q requests pytz

echo ""
echo "Running daily_check.py..."
echo "=============================="
python .github/scripts/daily_check.py

echo ""
echo "=============================="
echo "Running weekly_check.py..."
echo "=============================="
python .github/scripts/weekly_check.py

echo ""
echo "=============================="
echo "Tests completed!"
