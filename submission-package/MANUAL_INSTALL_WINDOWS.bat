@echo off
REM Simple Windows Manual Install Guide

echo ========================================
echo Manual Installation for Windows
echo ========================================
echo.

echo If the automatic RUN_ON_WINDOWS.bat fails, try these commands manually:
echo.

echo 1. First, update pip:
echo    python -m pip install --upgrade pip
echo.

echo 2. Then install required packages:
echo    pip install matplotlib pandas pillow
echo.

echo 3. If that fails, try with --user flag:
echo    pip install --user matplotlib pandas pillow
echo.

echo 4. If you still have issues, try:
echo    python -m pip install matplotlib pandas pillow
echo.

echo 5. Finally, run the dashboard:
echo    python dashboard.py
echo.

echo ========================================
echo Copy and paste these commands one by one
echo into Command Prompt if needed
echo ========================================

pause
