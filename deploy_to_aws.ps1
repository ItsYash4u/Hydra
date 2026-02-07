# deploy_to_aws.ps1
# This script automates the deployment of Greeva to AWS EC2.

$IP = "54.173.213.113"
$USER = "ubuntu"
$PEM_FILE = "hydroponics_sys.pem"
$REMOTE_DIR = "~/greeva"

Write-Host "🚀 Starting Deployment to AWS EC2 ($IP)..." -ForegroundColor Cyan

# 1. Check for PEM file
if (-not (Test-Path $PEM_FILE)) {
    Write-Error "Pem file $PEM_FILE not found in current directory!"
    exit
}

# 2. Fix permissions on local Windows (Security requirement for OpenSSH)
Write-Host "🔧 Fixing .pem file permissions..."
icacls $PEM_FILE /inheritance:r
icacls $PEM_FILE /grant:r "$($env:USERNAME):(R)"

# 3. Create remote directory
Write-Host "📁 Creating remote directory..."
ssh -i $PEM_FILE -o StrictHostKeyChecking=no "$USER@$IP" "mkdir -p $REMOTE_DIR/nginx $REMOTE_DIR/scripts"

# 4. Copy files to EC2
Write-Host "📤 Transferring files to EC2..."
scp -i $PEM_FILE -o StrictHostKeyChecking=no docker-compose.yml Dockerfile .env "$USER@$IP`:$REMOTE_DIR/"
scp -i $PEM_FILE -o StrictHostKeyChecking=no nginx/nginx.conf "$USER@$IP`:$REMOTE_DIR/nginx/"
scp -i $PEM_FILE -o StrictHostKeyChecking=no scripts/setup_server.sh "$USER@$IP`:$REMOTE_DIR/scripts/"

# 5. Run setup and launch on EC2
Write-Host "⚙️ Setting up server and launching containers (this may take a few minutes)..."
ssh -i $PEM_FILE -o StrictHostKeyChecking=no "$USER@$IP" @"
    cd $REMOTE_DIR
    chmod +x scripts/setup_server.sh
    ./scripts/setup_server.sh
    # Refresh group membership for docker
    sudo docker compose up -d --build
"@

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "🌐 You can now access your dashboard at http://$IP" -ForegroundColor Cyan
