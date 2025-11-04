@echo off
REM ServiceGenie Quick Start Script for Windows
echo =============================
echo ServiceGenie - Quick Start
echo =============================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed or not in PATH
    pause
    exit /b
)

echo Setting up Backend...
cd Backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please configure your .env file with proper credentials
)

echo Installing backend dependencies...
pip install -q -r requirements.txt
echo Backend setup complete!
echo.

REM Frontend Setup
echo Setting up Frontend...
cd ..\Frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

if not exist ".env.local" (
    echo Creating .env.local file...
    copy .env.example .env.local
    echo Please configure your .env.local file with proper credentials
)

echo Frontend setup complete!
echo.

REM Ask to seed database
set /p seed_choice="Do you want to seed the database with sample data? (y/n): "
if /i "%seed_choice%"=="y" (
    cd ..\Backend
    call venv\Scripts\activate.bat
    python scripts\seed_db.py
)

echo.
echo Setup complete!
echo.
echo To start the application:
echo   1. Backend:  cd Backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo   2. Frontend: cd Frontend ^&^& npm run dev
echo.
echo Then open http://localhost:3000 in your browser
pause
