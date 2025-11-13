#!/bin/bash

# Stop Dashboard Script
# Cleanly stops the running dashboard

echo "⏹️  Stopping Dashboard..."

# Stop any existing instances
pkill -f "python.*dashboard.py" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Dashboard stopped successfully."
else
    echo "ℹ️  No dashboard instances were running."
fi
