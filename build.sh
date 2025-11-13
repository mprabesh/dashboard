#!/bin/bash

# Build script for Python Dashboard
# This script creates a standalone executable using PyInstaller

echo "🚀 Building Python Dashboard Application..."

# Check if virtual environment exists
if [ ! -d "dashboard_env" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Activate virtual environment
source dashboard_env/bin/activate

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
if [ -d "dist" ]; then
    echo "🧹 Cleaning previous builds..."
    rm -rf dist/
fi

if [ -d "build" ]; then
    rm -rf build/
fi

if [ -f "dashboard.spec" ]; then
    rm dashboard.spec
fi

# Build the application
echo "🔧 Building standalone executable..."
pyinstaller --onefile \
    --name="ArcticDataSolutions-Dashboard" \
    --add-data="*.csv:." \
    --windowed \
    dashboard.py

# Check if build was successful
if [ -f "dist/ArcticDataSolutions-Dashboard" ]; then
    echo "✅ Build successful!"
    echo "📦 Executable created: dist/ArcticDataSolutions-Dashboard"
    echo "💡 You can now run: ./dist/ArcticDataSolutions-Dashboard"
    
    # Make the executable... executable
    chmod +x dist/ArcticDataSolutions-Dashboard
    
    # Show file size
    echo "📊 File size: $(du -h dist/ArcticDataSolutions-Dashboard | cut -f1)"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 Dashboard build complete!"
