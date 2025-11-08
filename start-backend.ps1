# ServiceGenie Backend Startup Script
Write-Host "Starting Backend Server..." -ForegroundColor Green

cd "C:\Users\mahin\OneDrive_BUET\Desktop\New folder\ServiceGenie\Backend"

# Set minimal environment variables for prototype
$env:MONGO_URI = "mongodb://localhost:27017"
$env:DATABASE_NAME = "servicegenie"
$env:ENVIRONMENT = "development"
$env:FIREBASE_PROJECT_ID = "dev"
$env:FIREBASE_CREDENTIAL_PATH = "dev"

Write-Host "Environment variables set" -ForegroundColor Yellow
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start the server
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

