@echo off
REM Arctic Data Solutions Dashboard - Simple Windows Launcher
REM This version skips complex verification and just runs the dashboard

echo.
echo ========================================
echo Arctic Data Solutions Dashboard
echo Simple Windows Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if dashboard.py exists
if not exist "dashboard.py" (
    echo ❌ dashboard.py not found! Make sure you're in the correct directory
    pause
    exit /b 1
)

REM Quick package check and install if needed
echo.
echo 📦 Ensuring required packages are installed...
pip install matplotlib pandas pillow --quiet --disable-pip-version-check

REM Count CSV files
echo.
echo 📊 Checking CSV files...
set csv_count=0
for %%f in (*.csv) do set /a csv_count+=1
echo ✅ Found %csv_count% CSV data files

REM Run the dashboard directly
echo.
echo 🚀 Starting Arctic Data Solutions Dashboard...
echo    (Your packages are already installed - they should work!)
echo.

python dashboard.py

echo.
echo 👋 Dashboard session complete!
pause
