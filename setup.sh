#!/bin/bash
# ==============================================================
# Arrodes Bot - Oracle Cloud One-Shot Setup Script
# Run this once on a fresh Ubuntu 22.04 VM:
#   bash <(curl -fsSL https://raw.githubusercontent.com/Theroid00/Arrodes/main/setup.sh)
# ==============================================================

set -e  # Exit immediately on any error

echo "================================================"
echo "   Arrodes Discord Bot - Oracle Cloud Setup"
echo "================================================"

# ── 1. System update & Dependency check ─────────────────────
echo "[1/6] Updating system packages and checking dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -qq && sudo apt-get upgrade -y -qq
    if ! command -v git &> /dev/null; then
        sudo apt-get install -y -qq git
    fi
elif command -v dnf &> /dev/null; then
    sudo dnf update -y -q
    if ! command -v git &> /dev/null; then
        sudo dnf install -y -q git
    fi
elif command -v yum &> /dev/null; then
    sudo yum update -y -q
    if ! command -v git &> /dev/null; then
        sudo yum install -y -q git
    fi
fi

# ── 2. Install Docker ───────────────────────────────────────
echo "[2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sudo sh
    if command -v systemctl &> /dev/null; then
        sudo systemctl enable --now docker
    fi
    sudo usermod -aG docker "$USER"
    echo "      Docker installed and service started."
else
    echo "      Docker already installed, skipping."
fi

# ── 3. Install Docker Compose ───────────────────────────────
echo "[3/6] Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "      Docker Compose installed."
else
    echo "      Docker Compose already installed, skipping."
fi

# ── 4. Clone the repo ───────────────────────────────────────
echo "[4/6] Cloning Arrodes repository..."
REPO_DIR="$HOME/Arrodes"
if [ -d "$REPO_DIR" ]; then
    echo "      Repo already exists. Pulling latest changes..."
    git -C "$REPO_DIR" pull
else
    git clone https://github.com/Theroid00/Arrodes.git "$REPO_DIR"
fi
cd "$REPO_DIR"

# ── 5. Create .env file ─────────────────────────────────────
echo "[5/6] Setting up environment variables..."
if [ ! -f ".env" ]; then
    echo ""
    read -rp "  Enter your Discord BOT_TOKEN: " BOT_TOKEN
    echo "BOT_TOKEN=$BOT_TOKEN" > .env
    echo "      .env file created."
else
    echo "      .env file already exists, skipping."
fi

# ── 6. Build and launch the bot ─────────────────────────────
echo "[6/6] Building Docker image and starting the bot..."
# Run docker-compose
sudo docker-compose up --build -d

echo ""
echo "================================================"
echo "   ✅  Arrodes is running! (auto-restarts on crash)"
echo ""
echo "   Useful commands:"
echo "   View live logs :  sudo docker-compose -f $REPO_DIR/docker-compose.yml logs -f"
echo "   Stop the bot   :  sudo docker-compose -f $REPO_DIR/docker-compose.yml down"
echo "   Update the bot :  cd $REPO_DIR && git pull && sudo docker-compose up --build -d"
echo "================================================"
