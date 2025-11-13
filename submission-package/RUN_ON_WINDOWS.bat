@echo off
REM Arctic Data Solutions Dashboard - Windows Setup and Run Script

echo.
echo ========================================
echo Arctic Data Solutions Dashboard
echo Windows Setup and Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+ from python.org
    echo    Download: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if required files exist
if not exist "dashboard.py" (
    echo ❌ dashboard.py not found! Make sure you're in the correct directory
    pause
    exit /b 1
)

REM Install required packages
echo.
echo 📦 Installing required packages...
echo    Note: tkinter comes with Python on Windows, no need to install separately

pip install matplotlib pandas pillow

REM Check if installation was successful
python -c "import matplotlib, pandas; print('✅ All packages installed successfully')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Package installation failed! Trying with --user flag...
    pip install --user matplotlib pandas pillow
    python -c "import matplotlib, pandas; print('✅ Packages installed with --user flag')" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Installation still failed! Please check your Python/pip setup
        echo    Try running: python -m pip install --upgrade pip
        echo    Then: pip install matplotlib pandas pillow
        pause
        exit /b 1
    )
)

REM Check if CSV files exist
echo.
echo 📊 Checking for Arctic Data Solutions CSV files...
set csv_count=0
for %%f in (*.csv) do set /a csv_count+=1

if %csv_count% LSS 7 (
    echo ⚠️  Warning: Expected 7 CSV files, found %csv_count%
    echo    Make sure all Arctic Data Solutions data files are present
)

echo ✅ Found %csv_count% CSV data files

REM Verify all required packages are available
echo.
echo 🔍 Verifying all required packages are installed...
python -c "import tkinter, matplotlib.pyplot, pandas; print('✅ All packages verified and ready')"
if errorlevel 1 (
    echo ❌ Some required packages are missing or not working
    echo    Please check the error messages above and install missing packages
    pause
    exit /b 1
)

REM Run the dashboard
echo.
echo 🚀 Starting Arctic Data Solutions Dashboard...
echo    Close the dashboard window to return to this prompt
echo.

python dashboard.py

echo.
echo 👋 Dashboard closed. Thanks for using Arctic Data Solutions Dashboard!
pause
