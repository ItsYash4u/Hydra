#!/bin/bash
# AWS_EC2_DEPLOYMENT_COMMANDS.sh
# Copy and paste these commands into your AWS EC2 Instance Connect web terminal

# Step 1: Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo apt-get update
    sudo apt-get install -y git
fi

# Step 2: Clone your repository
# Replace YOUR_GITHUB_USERNAME and YOUR_REPO_NAME with actual values
echo "Cloning repository..."
cd ~
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Step 3: Install Docker and Docker Compose
echo "Installing Docker..."
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin

# Step 4: Start Docker service
echo "Starting Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Step 5: Build and launch the application
echo "Building and launching containers..."
sudo docker compose up -d --build

# Step 6: Check deployment status
echo "Checking deployment status..."
sleep 5
sudo docker compose ps

echo ""
echo "========================================"
echo "✅ Deployment Complete!"
echo "========================================"
echo "Your dashboard should be accessible at:"
echo "http://54.173.213.113"
echo ""
echo "To view logs, run:"
echo "  sudo docker compose logs -f"
echo ""
