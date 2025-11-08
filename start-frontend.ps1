# ServiceGenie Frontend Startup Script
Write-Host "Starting Frontend Server..." -ForegroundColor Green

cd "C:\Users\mahin\OneDrive_BUET\Desktop\New folder\ServiceGenie\Frontend"

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting Next.js dev server on http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start the server
npm run dev

