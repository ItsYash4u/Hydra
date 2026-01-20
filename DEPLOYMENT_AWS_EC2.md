# 🚀 AWS EC2 Deployment Guide - Smart IoT Hydroponics Dashboard

Complete step-by-step guide to deploy your Django application on AWS EC2.

---

## 📋 **TABLE OF CONTENTS**

1. [Prerequisites](#prerequisites)
2. [AWS EC2 Setup](#aws-ec2-setup)
3. [Server Configuration](#server-configuration)
4. [Database Setup](#database-setup)
5. [Application Deployment](#application-deployment)
6. [Nginx & Gunicorn Setup](#nginx--gunicorn-setup)
7. [SSL Certificate (HTTPS)](#ssl-certificate-https)
8. [Domain Configuration](#domain-configuration)
9. [Troubleshooting](#troubleshooting)

---

## 📦 **PREREQUISITES**

Before starting, ensure you have:
- ✅ AWS Account with billing enabled
- ✅ SSH client (PuTTY for Windows or Terminal for Mac/Linux)
- ✅ Your Django project code
- ✅ Domain name (optional, for custom URL)

---

## 🖥️ **PART 1: AWS EC2 SETUP**

### **Step 1: Launch EC2 Instance**

1. **Login to AWS Console**
   - Go to https://console.aws.amazon.com/
   - Navigate to EC2 Dashboard

2. **Launch Instance**
   - Click "Launch Instance"
   - **Name**: `hydroponics-dashboard`

3. **Choose AMI (Operating System)**
   - Select: **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type**
   - Architecture: **64-bit (x86)**

4. **Choose Instance Type**
   - Recommended: **t2.micro** (Free tier eligible)
   - Or: **t2.small** (Better performance, ~$17/month)
   - Or: **t3.micro** (Better CPU performance)

5. **Key Pair (Login)**
   - Click "Create new key pair"
   - **Name**: `hydroponics-key`
   - **Type**: RSA
   - **Format**: `.pem` (for Mac/Linux) or `.ppk` (for PuTTY/Windows)
   - **Download and save securely!** (You can't download it again)

6. **Network Settings**
   - ✅ Allow SSH traffic from: **My IP** (or Anywhere for testing)
   - ✅ Allow HTTP traffic from: **Internet**
   - ✅ Allow HTTPS traffic from: **Internet**

7. **Configure Storage**
   - **Size**: 20 GB (minimum)
   - **Type**: gp3 (General Purpose SSD)

8. **Launch Instance**
   - Click "Launch Instance"
   - Wait 2-3 minutes for instance to start

9. **Get Instance Details**
   - Click on your instance
   - Note down:
     - **Public IPv4 address**: (e.g., 54.123.45.67)
     - **Public IPv4 DNS**: (e.g., ec2-54-123-45-67.compute-1.amazonaws.com)

---

### **Step 2: Configure Security Group**

1. **Go to Security Groups**
   - EC2 Dashboard → Security Groups
   - Select your instance's security group

2. **Edit Inbound Rules**
   - Click "Edit inbound rules"
   - Add these rules:

   | Type | Protocol | Port | Source | Description |
   |------|----------|------|--------|-------------|
   | SSH | TCP | 22 | My IP | SSH access |
   | HTTP | TCP | 80 | 0.0.0.0/0 | Web traffic |
   | HTTPS | TCP | 443 | 0.0.0.0/0 | Secure web |
   | Custom TCP | TCP | 8000 | 0.0.0.0/0 | Django dev (temp) |
   | MySQL | TCP | 3306 | My IP | Database (optional) |

3. **Save Rules**

---

### **Step 3: Connect to EC2 Instance**

#### **For Windows (Using PuTTY):**

1. **Convert .pem to .ppk** (if needed)
   - Download PuTTYgen
   - Load your `.pem` file
   - Save as `.ppk`

2. **Connect with PuTTY**
   - Host: `ubuntu@YOUR_PUBLIC_IP`
   - Port: 22
   - Connection → SSH → Auth → Browse for `.ppk` file
   - Click "Open"

#### **For Mac/Linux:**

```bash
# Set permissions
chmod 400 hydroponics-key.pem

# Connect
ssh -i hydroponics-key.pem ubuntu@YOUR_PUBLIC_IP
```

**Example**:
```bash
ssh -i hydroponics-key.pem ubuntu@54.123.45.67
```

---

## ⚙️ **PART 2: SERVER CONFIGURATION**

### **Step 1: Update System**

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y build-essential git curl wget vim
```

### **Step 2: Install Python 3.12**

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Install pip
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# Verify installation
python3.12 --version
pip3.12 --version
```

### **Step 3: Install MySQL Server**

```bash
# Install MySQL
sudo apt install -y mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation
sudo mysql_secure_installation
```

**MySQL Secure Installation Prompts**:
- Validate password component? **Y**
- Password strength: **2** (Strong)
- Set root password: **YOUR_STRONG_PASSWORD** (save this!)
- Remove anonymous users? **Y**
- Disallow root login remotely? **Y**
- Remove test database? **Y**
- Reload privilege tables? **Y**

### **Step 4: Install Nginx**

```bash
# Install Nginx
sudo apt install -y nginx

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

**Test**: Open `http://YOUR_PUBLIC_IP` in browser - You should see "Welcome to nginx!"

---

## 🗄️ **PART 3: DATABASE SETUP**

### **Step 1: Create MySQL Database**

```bash
# Login to MySQL
sudo mysql -u root -p
```

**In MySQL prompt**:
```sql
-- Create database
CREATE DATABASE hydroponics_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'hydroponics_user'@'localhost' IDENTIFIED BY 'YOUR_DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON hydroponics_db.* TO 'hydroponics_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

### **Step 2: Install MySQL Client Library**

```bash
# Install MySQL development files
sudo apt install -y libmysqlclient-dev pkg-config
```

---

## 📦 **PART 4: APPLICATION DEPLOYMENT**

### **Step 1: Clone Your Project**

```bash
# Navigate to home directory
cd ~

# Clone from GitHub (if using Git)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git hydroponics

# OR upload via SCP (from your local machine)
# scp -i hydroponics-key.pem -r /path/to/Greeva ubuntu@YOUR_PUBLIC_IP:~/hydroponics
```

**If uploading manually**:
```bash
# On your local machine (Windows PowerShell or Mac/Linux Terminal)
scp -i hydroponics-key.pem -r "C:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva" ubuntu@YOUR_PUBLIC_IP:~/hydroponics
```

### **Step 2: Set Up Virtual Environment**

```bash
# Navigate to project
cd ~/hydroponics

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### **Step 3: Install Dependencies**

```bash
# Install requirements
pip install -r requirements.txt

# Install additional production packages
pip install gunicorn mysqlclient python-dotenv
```

### **Step 4: Create Environment File**

```bash
# Create .env file
nano ~/hydroponics/.env
```

**Add this content** (replace with your values):
```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=YOUR_PUBLIC_IP,YOUR_DOMAIN.com,www.YOUR_DOMAIN.com

# Database Settings
DB_NAME=hydroponics_db
DB_USER=hydroponics_user
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=localhost
DB_PORT=3306

# Email Settings (for OTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Save**: Press `Ctrl+X`, then `Y`, then `Enter`

### **Step 5: Update Django Settings**

```bash
# Edit settings.py
nano ~/hydroponics/greeva/greeva/settings.py
```

**Update these sections**:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'hydroponics_db'),
        'USER': os.getenv('DB_USER', 'hydroponics_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### **Step 6: Collect Static Files**

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### **Step 7: Run Migrations**

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### **Step 8: Create Superuser**

```bash
# Create admin user
python manage.py createsuperuser
```

**Enter**:
- Email: `yashsinghkushwaha345@gmail.com`
- Password: `YOUR_ADMIN_PASSWORD`

### **Step 9: Test Django**

```bash
# Test run
python manage.py runserver 0.0.0.0:8000
```

**Test**: Open `http://YOUR_PUBLIC_IP:8000` in browser

**Stop server**: Press `Ctrl+C`

---

## 🔧 **PART 5: NGINX & GUNICORN SETUP**

### **Step 1: Create Gunicorn Service**

```bash
# Create systemd service file
sudo nano /etc/systemd/system/gunicorn.service
```

**Add this content**:
```ini
[Unit]
Description=Gunicorn daemon for Hydroponics Dashboard
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/hydroponics/greeva
Environment="PATH=/home/ubuntu/hydroponics/venv/bin"
ExecStart=/home/ubuntu/hydroponics/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/hydroponics/gunicorn.sock \
          greeva.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Save**: `Ctrl+X`, `Y`, `Enter`

### **Step 2: Start Gunicorn**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start Gunicorn
sudo systemctl start gunicorn

# Enable on boot
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn
```

### **Step 3: Configure Nginx**

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/hydroponics
```

**Add this content**:
```nginx
server {
    listen 80;
    server_name YOUR_PUBLIC_IP YOUR_DOMAIN.com www.YOUR_DOMAIN.com;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/hydroponics/greeva/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/hydroponics/greeva/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/hydroponics/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

**Save**: `Ctrl+X`, `Y`, `Enter`

### **Step 4: Enable Nginx Site**

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/hydroponics /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### **Step 5: Set Permissions**

```bash
# Add ubuntu to www-data group
sudo usermod -a -G www-data ubuntu

# Set permissions
sudo chown -R ubuntu:www-data ~/hydroponics
sudo chmod -R 755 ~/hydroponics
```

---

## 🔒 **PART 6: SSL CERTIFICATE (HTTPS)**

### **Step 1: Install Certbot**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx
```

### **Step 2: Get SSL Certificate**

**If you have a domain**:
```bash
# Get certificate
sudo certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com
```

**Follow prompts**:
- Email: Your email
- Agree to terms: **Y**
- Share email: **N** (optional)
- Redirect HTTP to HTTPS: **2** (Yes)

### **Step 3: Auto-Renewal**

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot will auto-renew every 90 days
```

---

## 🌐 **PART 7: DOMAIN CONFIGURATION**

### **Step 1: Point Domain to EC2**

In your domain registrar (GoDaddy, Namecheap, etc.):

1. **Add A Record**:
   - Type: **A**
   - Name: **@**
   - Value: **YOUR_EC2_PUBLIC_IP**
   - TTL: **3600**

2. **Add WWW Record**:
   - Type: **A**
   - Name: **www**
   - Value: **YOUR_EC2_PUBLIC_IP**
   - TTL: **3600**

### **Step 2: Update Django Settings**

```bash
nano ~/hydroponics/.env
```

**Update**:
```env
ALLOWED_HOSTS=YOUR_PUBLIC_IP,YOUR_DOMAIN.com,www.YOUR_DOMAIN.com
```

**Restart Gunicorn**:
```bash
sudo systemctl restart gunicorn
```

---

## 🔄 **UPDATING YOUR APPLICATION**

### **Method 1: Git Pull**

```bash
cd ~/hydroponics
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### **Method 2: Manual Upload**

```bash
# From local machine
scp -i hydroponics-key.pem -r /path/to/updated/files ubuntu@YOUR_PUBLIC_IP:~/hydroponics/

# On server
cd ~/hydroponics
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## 🛠️ **TROUBLESHOOTING**

### **Check Logs**

```bash
# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Django logs (if configured)
tail -f ~/hydroponics/greeva/logs/django.log
```

### **Common Issues**

#### **1. 502 Bad Gateway**
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Restart Gunicorn
sudo systemctl restart gunicorn

# Check socket file
ls -l ~/hydroponics/gunicorn.sock
```

#### **2. Static Files Not Loading**
```bash
# Recollect static files
cd ~/hydroponics/greeva
source ~/hydroponics/venv/bin/activate
python manage.py collectstatic --noinput

# Check permissions
sudo chown -R ubuntu:www-data ~/hydroponics/greeva/staticfiles
sudo chmod -R 755 ~/hydroponics/greeva/staticfiles
```

#### **3. Database Connection Error**
```bash
# Test MySQL connection
mysql -u hydroponics_user -p hydroponics_db

# Check MySQL status
sudo systemctl status mysql

# Restart MySQL
sudo systemctl restart mysql
```

#### **4. Permission Denied**
```bash
# Fix permissions
sudo chown -R ubuntu:www-data ~/hydroponics
sudo chmod -R 755 ~/hydroponics

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 📊 **MONITORING**

### **Check Service Status**

```bash
# All services
sudo systemctl status gunicorn nginx mysql

# Individual services
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status mysql
```

### **Resource Usage**

```bash
# CPU and Memory
htop

# Disk usage
df -h

# Check processes
ps aux | grep gunicorn
```

---

## 🎯 **FINAL CHECKLIST**

- ✅ EC2 instance running
- ✅ Security groups configured
- ✅ Python 3.12 installed
- ✅ MySQL database created
- ✅ Django project deployed
- ✅ Gunicorn service running
- ✅ Nginx configured
- ✅ SSL certificate installed (if using domain)
- ✅ Static files collected
- ✅ Database migrated
- ✅ Application accessible via browser

---

## 🌟 **YOUR DASHBOARD IS LIVE!**

Access your dashboard at:
- **HTTP**: `http://YOUR_PUBLIC_IP`
- **HTTPS** (with domain): `https://YOUR_DOMAIN.com`

**Admin Panel**: `https://YOUR_DOMAIN.com/admin/`

---

## 📞 **SUPPORT**

If you encounter issues:
1. Check logs (see Troubleshooting section)
2. Verify all services are running
3. Check security group rules
4. Ensure .env file has correct values

**Congratulations! Your Smart IoT Hydroponics Dashboard is now live on AWS EC2!** 🎉
