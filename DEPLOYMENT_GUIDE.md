# Flowchart Web Application - Deployment Guide

This guide provides multiple ways to deploy the Flowchart Web Application.

## Quick Start Options

### Option 1: Simple Python Setup (Recommended for Development)
1. **Run the batch file**: `run_web_app.bat`
2. **Access**: http://localhost:5000

### Option 2: Docker Deployment (Recommended for Production)
1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop
2. **Run the Docker batch file**: `run_docker.bat`
3. **Access**: http://localhost:5000

### Option 3: Manual Python Setup
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r web_requirements.txt
python app.py
```

## Deployment Options

### 1. Local Development
```cmd
# Development mode with auto-reload
set FLASK_ENV=development
python app.py
```

### 2. Local Network Access
To make the app accessible from other devices on your network:
- Edit `app.py` line 120: `app.run(debug=True, host='0.0.0.0', port=5000)`
- Access via: `http://YOUR_IP_ADDRESS:5000`

### 3. Production with Gunicorn
```cmd
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### 4. Docker Deployment
```cmd
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t flowchart-web .
docker run -p 5000:5000 flowchart-web
```

### 5. Cloud Deployment

#### Heroku
1. **Create Heroku app**:
   ```cmd
   heroku create your-app-name
   ```

2. **Create Procfile**:
   ```
   web: gunicorn app:app
   ```

3. **Deploy**:
   ```cmd
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

#### AWS EC2
1. **Launch EC2 instance** (Ubuntu/Amazon Linux)
2. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Upload files and run**:
   ```bash
   sudo docker-compose up -d
   ```

#### Azure Container Instances
1. **Create resource group**:
   ```bash
   az group create --name flowchart-rg --location eastus
   ```

2. **Deploy container**:
   ```bash
   az container create \
     --resource-group flowchart-rg \
     --name flowchart-web \
     --image your-registry/flowchart-web:latest \
     --ports 5000 \
     --ip-address public
   ```

### 6. Reverse Proxy with Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Environment Variables

You can configure the application using environment variables:

```cmd
set FLASK_ENV=production
set FLASK_HOST=0.0.0.0
set FLASK_PORT=5000
set FLASK_DEBUG=False
```

## Security Considerations

### For Production:
1. **Set secure secret key**:
   ```python
   app.secret_key = 'your-secure-secret-key-here'
   ```

2. **Enable HTTPS** with SSL certificates

3. **Use environment variables** for sensitive data

4. **Set up firewall rules** to restrict access

5. **Regular updates** of dependencies

## Performance Optimization

### 1. Gunicorn Configuration
```cmd
gunicorn -w 4 \
  --worker-class gevent \
  --worker-connections 1000 \
  --timeout 120 \
  --keep-alive 2 \
  --bind 0.0.0.0:5000 \
  app:app
```

### 2. Caching
Add caching headers for static files:
```python
@app.after_request
def add_cache_headers(response):
    if request.endpoint == 'static':
        response.cache_control.max_age = 86400  # 1 day
    return response
```

### 3. Load Balancing
Use nginx or HAProxy for load balancing multiple instances.

## Monitoring and Logging

### 1. Application Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 2. Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': time.time()}
```

### 3. Monitoring Tools
- **Application**: New Relic, Datadog
- **Infrastructure**: Prometheus + Grafana
- **Uptime**: Pingdom, UptimeRobot

## Backup and Recovery

### Database Backup
If you add a database later:
```bash
# PostgreSQL
pg_dump -h localhost -U username dbname > backup.sql

# MySQL
mysqldump -u username -p dbname > backup.sql
```

### File System Backup
```bash
# Backup uploaded files
tar -czf uploads_backup.tar.gz uploads/
```

## Troubleshooting

### Common Issues

1. **Port 5000 in use**:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Permission denied**:
   ```cmd
   # Run as administrator
   # Or change port to 8000+
   ```

3. **Memory issues**:
   ```cmd
   # Increase worker memory
   gunicorn --worker-class gevent --worker-connections 100 app:app
   ```

4. **Font loading issues**:
   ```bash
   # Check font file permissions
   ls -la fonts/
   ```

### Debug Mode
```python
# Enable debug mode
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Logs
```bash
# View Docker logs
docker-compose logs -f

# View application logs
tail -f app.log
```

## Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
version: '3.8'
services:
  flowchart-web:
    build: .
    ports:
      - "5000-5003:5000"
    deploy:
      replicas: 4
```

### Vertical Scaling
```yaml
# Increase resources
services:
  flowchart-web:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

## Maintenance

### Regular Tasks
1. **Update dependencies**:
   ```cmd
   pip install -r web_requirements.txt --upgrade
   ```

2. **Clean temporary files**:
   ```cmd
   # Clean temp directory periodically
   del /q %TEMP%\temp_*.txt
   del /q %TEMP%\temp_*.png
   ```

3. **Monitor disk space**:
   ```cmd
   # Check disk usage
   dir /s
   ```

4. **Security updates**:
   ```cmd
   # Update system packages
   pip install --upgrade pip
   pip install --upgrade -r web_requirements.txt
   ```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Submit issues to the project repository
4. Check the README_WEB.md for usage instructions
