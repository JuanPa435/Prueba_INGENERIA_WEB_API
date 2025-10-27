# 🚀 Deployment Checklist

## Pre-Deployment

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] MySQL server accessible
- [ ] Virtual environment created
- [ ] All dependencies installed (`pip install -r requirements.txt`)

### Configuration
- [ ] `backend/.env` configured with production values
- [ ] Database created and accessible
- [ ] Strong SECRET_KEY set (not default)
- [ ] Strong JWT_SECRET_KEY set
- [ ] Database credentials secured

### Security
- [ ] Change default SECRET_KEY
- [ ] Change default JWT_SECRET_KEY  
- [ ] Ensure .env is in .gitignore
- [ ] Review CORS settings for production domains
- [ ] Enable HTTPS in production
- [ ] Set secure cookie flags if using sessions

### Testing
- [ ] All authentication flows tested
- [ ] Company creation tested
- [ ] Product CRUD tested
- [ ] Role-based access verified
- [ ] Multi-tenant isolation verified
- [ ] JWT expiration tested
- [ ] Error handling tested

---

## Deployment Steps

### Backend Deployment

#### Option 1: Traditional Server (Ubuntu/Debian)

1. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv mysql-server nginx
```

2. **Setup project:**
```bash
cd /var/www
git clone <repository>
cd Prueba_INGENERIA_WEB_API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
nano backend/.env
# Set production values
```

4. **Setup systemd service:**
```bash
sudo nano /etc/systemd/system/inventory-api.service
```

```ini
[Unit]
Description=Inventory Management API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/Prueba_INGENERIA_WEB_API/backend
Environment="PATH=/var/www/Prueba_INGENERIA_WEB_API/venv/bin"
ExecStart=/var/www/Prueba_INGENERIA_WEB_API/venv/bin/python Main.py

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable inventory-api
sudo systemctl start inventory-api
```

5. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/inventory-api
```

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/inventory-api /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Option 2: Docker

1. **Create Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/

ENV FLASK_APP=Main.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "Main.py"]
```

2. **Build and run:**
```bash
docker build -t inventory-api .
docker run -d -p 5000:5000 --env-file backend/.env inventory-api
```

#### Option 3: Cloud Platform (Heroku, Railway, etc.)

Follow platform-specific deployment guides. Generally:
- Connect GitHub repository
- Set environment variables in dashboard
- Deploy from branch

### Frontend Deployment

#### Option 1: Static Hosting (Netlify, Vercel, GitHub Pages)

1. **Update API URL:**
```javascript
// frontend/js/config.js
const API_BASE_URL = 'https://api.yourdomain.com/api';
```

2. **Deploy:**
- Push to GitHub
- Connect to hosting platform
- Deploy frontend folder

#### Option 2: Nginx Static Files

```bash
sudo cp -r frontend/* /var/www/html/inventory/
```

```nginx
server {
    listen 80;
    server_name inventory.yourdomain.com;

    root /var/www/html/inventory;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Post-Deployment

### Verification
- [ ] Backend health check: `curl https://api.yourdomain.com/`
- [ ] Frontend loads correctly
- [ ] Can register new user
- [ ] Can login
- [ ] Can create company
- [ ] Can manage products
- [ ] HTTPS certificate valid
- [ ] CORS working correctly

### Monitoring
- [ ] Setup error logging
- [ ] Setup access logging
- [ ] Monitor database connections
- [ ] Monitor API response times
- [ ] Setup alerts for errors

### Backups
- [ ] Database backup strategy
- [ ] Automated daily backups
- [ ] Backup restoration tested
- [ ] Code repository backed up

### Documentation
- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document maintenance procedures

---

## Production Recommendations

### Performance
- [ ] Enable database connection pooling
- [ ] Add Redis for caching
- [ ] Setup CDN for frontend assets
- [ ] Optimize database indexes
- [ ] Enable gzip compression

### Security
- [ ] SSL/TLS certificate installed
- [ ] Rate limiting enabled
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CSRF tokens if needed
- [ ] Security headers configured
- [ ] Regular security updates

### Scalability
- [ ] Load balancer configured
- [ ] Auto-scaling setup
- [ ] Database read replicas
- [ ] Monitoring and alerting
- [ ] Log aggregation

### Maintenance
- [ ] Automated updates
- [ ] Health checks
- [ ] Uptime monitoring
- [ ] Error tracking (Sentry, etc.)
- [ ] Performance monitoring

---

## Common Issues

### Backend won't start
- Check Python version: `python --version`
- Verify dependencies: `pip list`
- Check database connection
- Review logs: `systemctl status inventory-api`

### 502 Bad Gateway
- Backend service not running
- Check systemd service: `sudo systemctl status inventory-api`
- Check Nginx config: `sudo nginx -t`

### CORS Errors
- Update CORS settings in `backend/Src/App.py`
- Allow frontend domain
- Check preflight requests

### Database Connection Failed
- Verify MySQL is running
- Check credentials in `.env`
- Test connection: `mysql -h host -u user -p`

### JWT Errors
- Tokens might be expired
- Check SECRET_KEY matches
- Clear localStorage and login again

---

## Rollback Plan

If deployment fails:

1. **Revert code:**
```bash
git checkout previous-working-commit
```

2. **Restart services:**
```bash
sudo systemctl restart inventory-api
sudo systemctl restart nginx
```

3. **Restore database backup:**
```bash
mysql -u user -p database < backup.sql
```

---

## Success Criteria

Deployment is successful when:
- ✅ Backend responds to health checks
- ✅ Frontend loads without errors
- ✅ Users can register and login
- ✅ Products can be created and managed
- ✅ HTTPS is working
- ✅ No console errors
- ✅ Database connections stable
- ✅ Monitoring is active

---

## Support

For issues during deployment:
1. Check logs: `sudo journalctl -u inventory-api -f`
2. Review error messages
3. Verify configuration
4. Test database connectivity
5. Check firewall rules
6. Verify DNS settings

---

Good luck with your deployment! 🚀
