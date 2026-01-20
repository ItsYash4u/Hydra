# 🚀 AWS EC2 Deployment - Quick Reference

## 📋 **QUICK START CHECKLIST**

### **Phase 1: AWS Setup (15 minutes)**
- [ ] Launch Ubuntu 22.04 EC2 instance (t2.micro or t2.small)
- [ ] Download and save `.pem` key file
- [ ] Configure Security Group (ports: 22, 80, 443, 8000)
- [ ] Note Public IP address
- [ ] Connect via SSH

### **Phase 2: Server Setup (20 minutes)**
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Install Python 3.12
- [ ] Install MySQL Server
- [ ] Install Nginx
- [ ] Create MySQL database and user

### **Phase 3: Deploy Application (15 minutes)**
- [ ] Upload/clone project to `~/hydroponics`
- [ ] Create virtual environment
- [ ] Install requirements
- [ ] Create `.env` file with credentials
- [ ] Collect static files
- [ ] Run migrations
- [ ] Create superuser

### **Phase 4: Production Setup (20 minutes)**
- [ ] Configure Gunicorn service
- [ ] Configure Nginx
- [ ] Set file permissions
- [ ] Test application
- [ ] (Optional) Install SSL certificate

---

## ⚡ **ESSENTIAL COMMANDS**

### **Connect to Server**
```bash
ssh -i hydroponics-key.pem ubuntu@YOUR_PUBLIC_IP
```

### **Restart Services**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart mysql
```

### **Check Status**
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status mysql
```

### **View Logs**
```bash
# Gunicorn
sudo journalctl -u gunicorn -f

# Nginx
sudo tail -f /var/log/nginx/error.log
```

### **Update Application**
```bash
cd ~/hydroponics
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## 🔑 **IMPORTANT CREDENTIALS TO SAVE**

1. **EC2 Key Pair**: `hydroponics-key.pem` (NEVER LOSE THIS!)
2. **EC2 Public IP**: `_________________`
3. **MySQL Root Password**: `_________________`
4. **MySQL DB Name**: `hydroponics_db`
5. **MySQL User**: `hydroponics_user`
6. **MySQL Password**: `_________________`
7. **Django Secret Key**: `_________________`
8. **Django Admin Email**: `yashsinghkushwaha345@gmail.com`
9. **Django Admin Password**: `_________________`

---

## 🌐 **ACCESS URLS**

- **Dashboard**: `http://YOUR_PUBLIC_IP`
- **Admin Panel**: `http://YOUR_PUBLIC_IP/admin/`
- **API Endpoint**: `http://YOUR_PUBLIC_IP/api/`

---

## 🛠️ **COMMON FIXES**

### **502 Bad Gateway**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### **Static Files Not Loading**
```bash
cd ~/hydroponics/greeva
source ~/hydroponics/venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### **Database Connection Error**
```bash
# Check MySQL is running
sudo systemctl status mysql

# Restart MySQL
sudo systemctl restart mysql

# Test connection
mysql -u hydroponics_user -p hydroponics_db
```

### **Permission Issues**
```bash
sudo chown -R ubuntu:www-data ~/hydroponics
sudo chmod -R 755 ~/hydroponics
sudo systemctl restart gunicorn
```

---

## 📊 **COST ESTIMATE**

| Resource | Type | Monthly Cost |
|----------|------|--------------|
| EC2 Instance | t2.micro | $0 (Free tier) or $8.50 |
| EC2 Instance | t2.small | ~$17 |
| Storage (20GB) | gp3 | ~$2 |
| Data Transfer | First 100GB | Free |
| **Total** | t2.micro | **$2-10/month** |
| **Total** | t2.small | **$19-25/month** |

---

## 🎯 **NEXT STEPS AFTER DEPLOYMENT**

1. **Test Everything**
   - Login/Signup flow
   - Dashboard functionality
   - Add Device feature
   - Sensor data display

2. **Set Up Monitoring**
   - CloudWatch for EC2 metrics
   - Application logging
   - Error tracking

3. **Backup Strategy**
   - Database backups
   - Code backups
   - Automated snapshots

4. **Domain Setup** (Optional)
   - Purchase domain
   - Point to EC2 IP
   - Install SSL certificate

5. **Optimization**
   - Enable caching
   - Optimize database queries
   - CDN for static files

---

## 📞 **EMERGENCY CONTACTS**

- **AWS Support**: https://console.aws.amazon.com/support/
- **EC2 Dashboard**: https://console.aws.amazon.com/ec2/
- **Billing Dashboard**: https://console.aws.amazon.com/billing/

---

**Full detailed guide**: See `DEPLOYMENT_AWS_EC2.md`
