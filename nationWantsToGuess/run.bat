@echo off
REM Quick launcher script for Nation Wants to Guess scoring app
REM Just double-click this file to run the app!

echo.
echo ====================================================
echo  Nation Wants to Guess - Scoring System
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check dependencies
echo Checking dependencies...
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may not be installed
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the app
echo.
echo Starting app...
python frontend/main.py

pause
