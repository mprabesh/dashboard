#!/bin/bash

# Quick Dashboard Restart Script
# Stops any running dashboard and starts a new one

echo "🔄 Restarting Dashboard..."

# Change to the project directory
cd "$(dirname "$0")"

# Stop any existing instances
echo "⏹️  Stopping existing dashboard..."
pkill -f "python.*dashboard.py" 2>/dev/null || true
sleep 1

# Start the dashboard
echo "▶️  Starting new dashboard instance..."
./run_dashboard.sh
