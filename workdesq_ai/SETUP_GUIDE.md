# NLP-to-SQL WorkDesQ AI - Complete Setup Guide for Linux

## Overview
This guide will help you set up the NLP-to-SQL application on Linux using MySQL and Ollama LLM.

---

## Prerequisites

### System Requirements
- **OS**: Ubuntu/Debian Linux (or similar)
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for LLM)
- **Disk Space**: 5GB for LLM model

### Required Software
1. **Python 3.8+**
2. **MySQL Server** (not XAMPP)
3. **Ollama** (for LLM)
4. **Git** (optional)

---

## Step-by-Step Installation

### Step 1: Install MySQL on Linux

```bash
# Update package list
sudo apt update

# Install MySQL server
sudo apt install mysql-server -y

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation
sudo mysql_secure_installation
```

**During secure installation:**
- Set root password (remember this!)
- Remove anonymous users: Yes
- Disallow root login remotely: No (for local development)
- Remove test database: Yes
- Reload privilege tables: Yes

### Step 2: Configure MySQL Database

```bash
# Login to MySQL
sudo mysql -u root -p

# Create database
CREATE DATABASE workdesq_db_new;

# Grant privileges (replace 'yourpassword' with your actual password)
GRANT ALL PRIVILEGES ON workdesq_db_new.* TO 'root'@'localhost' IDENTIFIED BY 'yourpassword';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Import Database Schema

```bash
# Navigate to project directory
cd /home/systools/Desktop/NLP-to-SQL/workdesq_ai

# Import the SQL file
mysql -u root -p workdesq_db_new < workdesq_db_new.sql
```

### Step 4: Install Python and Dependencies

```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
pip3 --version
```

### Step 5: Run Automated Setup Script

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script (this will take 10-15 minutes)
./setup.sh
```

**What the script does:**
- Creates Python virtual environment
- Installs all Python dependencies
- Installs Ollama
- Downloads Llama 3.1 8B model (~4.7GB)

### Step 6: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env
```

**Update these values in `.env`:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=workdesq_db_new
DB_PORT=3306

OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=http://localhost:11434
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 7: Start Ollama Service

```bash
# Start Ollama in background
ollama serve &

# Verify model is available
ollama list
```

You should see `llama3.1:8b` in the list.

---

## Running the Application

### Method 1: Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

### Method 2: Custom Port

```bash
# Run on specific port (e.g., 8080)
streamlit run app.py --server.port 8080
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

---

## Testing the Application

### Example Queries to Try:

1. **"Show employees with productivity below 60%"**
2. **"Who are the top 10 most productive employees?"**
3. **"Show department-wise productivity performance"**
4. **"Which employees have more than 80% productivity?"**
5. **"List all employees from Sales department"**
6. **"Show employees with high idle time"**
7. **"What is the average productivity by location?"**

---

## Project Structure

```
workdesq_ai/
├── app.py                  # Main Streamlit application
├── query_router.py         # NLP to SQL conversion (LLM-based, no hardcoding)
├── sql_executor.py         # SQL execution with error handling
├── llm_answer.py           # Natural language response generation
├── db.py                   # Database connection (environment-based)
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
├── .env                   # Environment configuration (create from .env.example)
├── .env.example           # Example environment file
└── workdesq_db_new.sql    # Database schema
```

---

## Key Improvements Made

### 1. **Fully Dynamic SQL Generation**
- ✅ NO hard-coded queries
- ✅ LLM generates SQL in real-time based on user input
- ✅ Handles any type of question about the database

### 2. **Better LLM Prompting**
- ✅ Comprehensive database schema provided to LLM
- ✅ Clear instructions and examples
- ✅ Low temperature for consistent SQL generation
- ✅ Automatic cleanup of markdown formatting

### 3. **Improved Error Handling**
- ✅ Connection management with proper cleanup
- ✅ Detailed error messages
- ✅ Graceful fallbacks

### 4. **Linux-Compatible Configuration**
- ✅ Environment variables for all settings
- ✅ MySQL instead of XAMPP
- ✅ Systemd service compatibility

### 5. **Enhanced Natural Language Responses**
- ✅ Statistical summaries
- ✅ Key insights and patterns
- ✅ Professional formatting

---

## Troubleshooting

### Issue 1: MySQL Connection Error

```bash
# Check MySQL status
sudo systemctl status mysql

# Restart MySQL
sudo systemctl restart mysql

# Check MySQL error logs
sudo tail -f /var/log/mysql/error.log
```

### Issue 2: Ollama Not Running

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama manually
ollama serve &

# Check Ollama logs
journalctl -u ollama -f
```

### Issue 3: LLM Model Not Found

```bash
# Pull the model again
ollama pull llama3.1:8b

# Verify model
ollama list
```

### Issue 4: Python Import Errors

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 5: Port Already in Use

```bash
# Find process using port 8501
sudo lsof -i :8501

# Kill the process (replace PID)
kill -9 PID

# Or use different port
streamlit run app.py --server.port 8080
```

---

## Performance Optimization

### 1. Increase Ollama Context Window
```bash
# Edit Ollama config
export OLLAMA_NUM_CTX=4096
ollama serve &
```

### 2. Use GPU Acceleration (if available)
```bash
# Install CUDA drivers
sudo apt install nvidia-cuda-toolkit

# Restart Ollama to detect GPU
```

### 3. Database Indexing
```sql
-- Add indexes for better query performance
CREATE INDEX idx_userid ON userdata11(userid);
CREATE INDEX idx_status ON userdata11(status);
CREATE INDEX idx_depid ON userdetails(depid);
```

---

## Security Recommendations

1. **Change default MySQL root password**
2. **Don't commit `.env` file to version control**
3. **Use firewall to restrict MySQL access**
4. **Keep Ollama service local (don't expose externally)**
5. **Regularly update dependencies**

```bash
# Update all packages
pip install --upgrade -r requirements.txt
```

---

## Advanced Configuration

### Custom LLM Model

To use a different model (e.g., Llama 3.3):

```bash
# Pull different model
ollama pull llama3.3

# Update .env file
OLLAMA_MODEL=llama3.3
```

### Database Backup

```bash
# Backup database
mysqldump -u root -p workdesq_db_new > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u root -p workdesq_db_new < backup_20260115.sql
```

---

## Support & Resources

- **Ollama Documentation**: https://ollama.com/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **MySQL Documentation**: https://dev.mysql.com/doc/

---

## Quick Commands Reference

```bash
# Start everything
source venv/bin/activate
ollama serve &
streamlit run app.py

# Stop Ollama
pkill ollama

# Check logs
journalctl -u ollama -f

# Update project
git pull
pip install -r requirements.txt --upgrade

# Reset database
mysql -u root -p workdesq_db_new < workdesq_db_new.sql
```

---

**Setup Complete! 🎉**

Your NLP-to-SQL application is now ready to use with fully dynamic LLM-based query generation.
