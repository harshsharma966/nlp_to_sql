#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     WorkDesQ AI - Complete Installation Script               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  This script needs sudo privileges."
    echo "Please run: sudo ./install_all.sh"
    exit 1
fi

# Update package list
echo -e "\n[1/6] Updating package list..."
apt update

# Install MySQL
echo -e "\n[2/6] Installing MySQL Server..."
DEBIAN_FRONTEND=noninteractive apt install mysql-server -y

# Start MySQL service
echo -e "\n[3/6] Starting MySQL service..."
systemctl start mysql
systemctl enable mysql

# Install Ollama
echo -e "\n[4/6] Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✓ Ollama already installed"
fi

# Setup MySQL database
echo -e "\n[5/6] Setting up MySQL database..."
mysql -e "CREATE DATABASE IF NOT EXISTS workdesq_db_new;"
mysql -e "GRANT ALL PRIVILEGES ON workdesq_db_new.* TO 'root'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# Import database schema
if [ -f "workdesq_db_new.sql" ]; then
    echo "Importing database schema..."
    mysql workdesq_db_new < workdesq_db_new.sql
    echo "✓ Database imported"
else
    echo "⚠️  workdesq_db_new.sql not found, skipping import"
fi

# Start Ollama and download model
echo -e "\n[6/6] Starting Ollama and downloading Llama 3.3 70B model..."
sudo -u $SUDO_USER ollama serve > /dev/null 2>&1 &
sleep 5

echo "Downloading Llama 3.3 70B model (this will take time, ~40GB)..."
sudo -u $SUDO_USER ollama pull llama3.3:70b

echo -e "\n╔═══════════════════════════════════════════════════════════════╗"
echo "║     ✓ Installation Complete!                                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Update .env file: nano .env"
echo "   Set DB_PASSWORD= (empty for no password)"
echo "   Set OLLAMA_MODEL=llama3.3:70b"
echo ""
echo "2. Run: ./start.sh"
echo ""
