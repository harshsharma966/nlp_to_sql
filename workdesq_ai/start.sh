#!/bin/bash

echo "🚀 Starting WorkDesQ AI Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
else
    echo "✓ Ollama is already running"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your database credentials before continuing."
    exit 1
fi

# Start Streamlit app
echo "✓ Starting Streamlit application..."
echo "📊 Open http://localhost:8501 in your browser"
echo ""
streamlit run app.py
