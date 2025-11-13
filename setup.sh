#!/bin/bash

# Setup script for Python Dashboard Application
echo "🔧 Setting up Python Dashboard Application..."

# Check Python version
python_version=$(python3 --version 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Found $python_version"

# Install required system packages (including tkinter)
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-tk python3-dev python3-setuptools

# Verify tkinter installation
echo "🔍 Verifying tkinter installation..."
python3 -c "import tkinter; print('✅ tkinter is available')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter installation failed. Trying alternative installation..."
    sudo apt install -y python3-tkinter tk-dev
    python3 -c "import tkinter; print('✅ tkinter is now available')" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Could not install tkinter. Please install manually:"
        echo "   sudo apt install python3-tkinter python3-tk"
        exit 1
    fi
fi

# Check if virtual environment already exists
if [ -d "dashboard_env" ]; then
    echo "📂 Virtual environment already exists."
else
    echo "🛠️  Creating virtual environment..."
    python3 -m venv dashboard_env
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        echo "Try: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source dashboard_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing required packages..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully!"
    echo ""
    echo "🚀 You can now run the dashboard with:"
    echo "   ./run_dashboard.sh"
    echo "   or"
    echo "   source dashboard_env/bin/activate && python dashboard.py"
    echo ""
    echo "📖 Or read the README.md for more information."
else
    echo "❌ Failed to install dependencies."
    echo "Please check your internet connection and try again."
    exit 1
fi
