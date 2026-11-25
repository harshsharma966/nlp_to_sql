#!/bin/bash

echo "================================================"
echo "NLP-to-SQL WorkDesQ AI - Linux Setup Script"
echo "================================================"

# Check Python version
echo -e "\n[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
python3 --version

# Create virtual environment
echo -e "\n[2/6] Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo -e "\n[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo -e "\n[4/6] Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo -e "\n[5/6] Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Python packages installed"

# Install and setup Ollama
echo -e "\n[6/6] Setting up Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✓ Ollama installed"
else
    echo "✓ Ollama already installed"
fi

# Start Ollama service
echo -e "\nStarting Ollama service..."
ollama serve > /dev/null 2>&1 &
sleep 3

# Pull the LLM model
echo -e "\nDownloading Llama 3.1 8B model (this may take a while)..."
ollama pull llama3.1:8b
echo "✓ Model downloaded"

echo -e "\n================================================"
echo "✓ Setup completed successfully!"
echo "================================================"
echo -e "\nNext steps:"
echo "1. Configure MySQL database (run: mysql -u root -p < workdesq_db_new.sql)"
echo "2. Update .env file with your database credentials"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run the app: streamlit run app.py"
echo ""
