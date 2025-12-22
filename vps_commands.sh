#!/bin/bash
# ========================================
# VPS Deployment Commands
# Run this script on your VPS
# ========================================

BACKUP_DATE="20251222_102237"
PROJECT_PATH="/root/comparely"
BACKUP_PATH="/root/backups"

echo "========================================="
echo "  COMPARELY VPS Setup"
echo "========================================="
echo ""

# Create backup directory
echo "[1/8] Creating backup directory..."
mkdir -p $BACKUP_PATH

# Backup existing project
echo "[2/8] Backing up existing project..."
if [ -d "$PROJECT_PATH" ]; then
    echo "Existing project found. Creating backup..."
    tar -czf $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz -C /root comparely
    echo "Backup saved to: $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz"
    
    # Move old project
    mv $PROJECT_PATH $PROJECT_PATH_old_$BACKUP_DATE
    echo "Old project moved to: $PROJECT_PATH_old_$BACKUP_DATE"
else
    echo "No existing project found. Skipping backup."
fi

# Update system
echo "[3/8] Updating system..."
apt update
apt upgrade -y

# Install dependencies
echo "[4/8] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx git

# Clone project (if using Git)
echo "[5/8] Cloning project..."
cd /root
# Uncomment if you want to clone from GitHub:
# git clone https://github.com/reyzae/comparely.git

# If project already uploaded, skip to next step
if [ ! -d "$PROJECT_PATH" ]; then
    echo "ERROR: Project not found at $PROJECT_PATH"
    echo "Please upload the project first or clone from Git."
    exit 1
fi

# Setup virtual environment
echo "[6/8] Setting up virtual environment..."
cd $PROJECT_PATH
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "[7/8] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Setup .env
echo "[8/8] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "IMPORTANT: Edit .env file with your configuration!"
    echo "Run: nano .env"
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Initialize database: python scripts/utils/init_db.py"
echo "3. Create admin user: python scripts/utils/create_admin_simple.py"
echo "4. Setup systemd service (see DEPLOYMENT_VPS.md)"
echo "5. Setup Nginx (see DEPLOYMENT_VPS.md)"
echo ""
echo "Backup location: $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz"
echo ""
