#!/bin/bash

# Python Dashboard Launcher
# This script activates the virtual environment and runs the dashboard

echo "🚀 Starting Python Dashboard..."

# Change to the project directory
cd "$(dirname "$0")"

# Check for and stop any existing dashboard instances
echo "🔄 Checking for existing dashboard instances..."
pkill -f "python.*dashboard.py" 2>/dev/null || true
sleep 1  # Give it a moment to clean up

# Check if virtual environment exists
if [ ! -d "dashboard_env" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Activate virtual environment
source dashboard_env/bin/activate

# Check if dependencies are installed
if ! python -c "import matplotlib, pandas, numpy" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the dashboard
echo "🎯 Launching Dashboard GUI..."
python dashboard.py
EXIT_CODE=$?

echo "👋 Dashboard closed (exit code: $EXIT_CODE)."
