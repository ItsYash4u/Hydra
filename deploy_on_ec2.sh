#!/bin/bash
# deploy_on_ec2.sh - Run this directly in AWS EC2 Instance Connect Terminal

set -e  # Exit on any error

echo "========================================="
echo "🚀 Greeva IoT Dashboard Deployment"
echo "========================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -qq

# Install Docker and Docker Compose
echo "🐳 Installing Docker..."
sudo apt-get install -y docker.io docker-compose-plugin

# Start Docker service
echo "▶️  Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add ubuntu user to docker group
echo "👤 Configuring Docker permissions..."
sudo usermod -aG docker ubuntu

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/greeva
cd ~/greeva

# Create docker-compose.yml
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/greeva/media
    env_file:
      - .env
    expose:
      - 8000

  nginx:
    image: nginx:1.25-alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/greeva/media
    ports:
      - 80:80
      - 443:443
    depends_on:
      - web

volumes:
  static_volume:
  media_volume:
EOF

# Create nginx directory and config
echo "🌐 Creating nginx configuration..."
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
upstream greeva_app {
    server web:8000;
}

server {
    listen 80;
    server_name 54.173.213.113;

    location / {
        proxy_pass http://greeva_app;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/greeva/media/;
    }
}
EOF

echo "✅ Configuration files created!"
echo ""
echo "========================================="
echo "⏳ Next step: Upload your project files"
echo "========================================="
echo ""
echo "You now need to upload your project files to this directory."
echo "See the upload instructions that were provided."
