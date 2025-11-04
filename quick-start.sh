#!/bin/bash

# ServiceGenie Quick Start Script
echo "🧞 ServiceGenie - Quick Start"
echo "=============================="
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first."
    echo "   Run: mongod"
    exit 1
fi

echo "✅ MongoDB is running"
echo ""

# Backend Setup
echo "🔧 Setting up Backend..."
cd Backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please configure your .env file with proper credentials"
fi

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Frontend Setup
echo "🎨 Setting up Frontend..."
cd ../Frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
    echo "⚠️  Please configure your .env.local file with proper credentials"
fi

echo "✅ Frontend setup complete"
echo ""

# Ask to seed database
echo "📊 Do you want to seed the database with sample data? (y/n)"
read -r seed_choice
if [ "$seed_choice" = "y" ]; then
    cd ../Backend
    source venv/bin/activate
    python scripts/seed_db.py
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Backend:  cd Backend && uvicorn main:app --reload"
echo "  2. Frontend: cd Frontend && npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
