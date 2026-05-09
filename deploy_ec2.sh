#!/bin/bash
# ============================================================
# AWS EC2 Deployment Script - Healthcare Data Platform
# Run this script on your EC2 instance after SSH-ing in
# ============================================================

echo "=== Healthcare Data Platform - EC2 Setup ==="

# ─────────────────────────────────────────────
# STEP 1: Update system
# ─────────────────────────────────────────────
sudo apt-get update -y
sudo apt-get upgrade -y

# ─────────────────────────────────────────────
# STEP 2: Install Docker
# ─────────────────────────────────────────────
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
echo "Docker installed"

# ─────────────────────────────────────────────
# STEP 3: Install Python & pip
# ─────────────────────────────────────────────
sudo apt-get install -y python3 python3-pip
echo "Python installed"

# ─────────────────────────────────────────────
# STEP 4: Clone or upload your project
# ─────────────────────────────────────────────
# Option A - If using GitHub:
# git clone https://github.com/your-username/healthcare-platform.git
# cd healthcare-platform

# Option B - Upload files via SCP from your local machine:
# scp -i your-key.pem -r ./healthcare_platform ubuntu@YOUR-EC2-IP:~/

# ─────────────────────────────────────────────
# STEP 5: Run with Docker Compose
# ─────────────────────────────────────────────
cd ~/healthcare_platform
sudo docker-compose up -d --build
echo "Containers started"

# ─────────────────────────────────────────────
# STEP 6: Trigger ETL to load data into MongoDB
# ─────────────────────────────────────────────
sleep 5  # Wait for containers to start
curl -X POST http://localhost:5000/etl/run
echo "ETL pipeline triggered"

echo ""
echo "=== Deployment Complete ==="
echo "Flask API:      http://YOUR-EC2-IP:5000"
echo "MongoDB UI:     http://YOUR-EC2-IP:8081"
echo ""
echo "IMPORTANT: Open these ports in your EC2 Security Group:"
echo "  - Port 5000 (Flask API)"
echo "  - Port 8081 (MongoDB Express UI)"
echo "  - Port 27017 (MongoDB - internal only, do NOT expose publicly)"
