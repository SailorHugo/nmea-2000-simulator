# NMEA 2000 Simulator Deployment Guide

## Overview

This guide covers deploying the NMEA simulator to platforms that support direct TCP connections for navigation apps like OpenCPN. The application requires Node.js, PostgreSQL, and external port access.

## Quick Deploy Options

### 1. DigitalOcean App Platform (Easiest)

**Prerequisites:**
- DigitalOcean account
- GitHub repository with your code

**Steps:**
1. Push code to GitHub repository
2. Go to DigitalOcean → Apps → Create App
3. Connect your GitHub repository
4. Configure build settings:
   - **Build Command**: `npm run build`
   - **Run Command**: `npm start`
   - **Environment**: Node.js 20
5. Add PostgreSQL database addon
6. Set environment variables:
   - `NODE_ENV=production`
   - `DATABASE_URL` (provided by PostgreSQL addon)
7. Deploy

**Estimated Cost:** $12-25/month

### 2. Railway (Modern & Simple)

**Prerequisites:**
- Railway account
- GitHub repository

**Steps:**
1. Go to railway.app → New Project
2. Deploy from GitHub repository
3. Add PostgreSQL database
4. Configure environment variables:
   - `NODE_ENV=production`
   - `DATABASE_URL` (auto-configured)
5. Enable custom domain or use provided railway.app URL

**If you get "monorepo" error:**
1. Ensure `package.json`, `railway.json`, and `nixpacks.toml` are in repository root
2. In Railway settings, set Root Directory to `/` (empty)
3. Build Command: `npm run build`
4. Start Command: `npm start`

**Estimated Cost:** $5-20/month

### 3. Render (Free Tier Available)

**Prerequisites:**
- Render account
- GitHub repository

**Steps:**
1. Go to render.com → New Web Service
2. Connect GitHub repository
3. Configure service:
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Environment**: Node.js
4. Add PostgreSQL database (separate service)
5. Set environment variables

**Estimated Cost:** Free tier available, paid plans from $7/month

### 4. VPS Deployment (Full Control)

**Recommended Providers:**
- **Linode**: $5-10/month
- **DigitalOcean Droplet**: $6-12/month
- **Vultr**: $5-10/month
- **Hetzner**: $4-8/month

## VPS Manual Setup Guide

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install PM2 for process management
sudo npm install -g pm2
```

### Step 2: Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE nmea_simulator;
CREATE USER nmea_user WITH ENCRYPTED PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE nmea_simulator TO nmea_user;
\q
```

### Step 3: Deploy Application

```bash
# Clone your repository
git clone https://github.com/yourusername/nmea-simulator.git
cd nmea-simulator

# Install dependencies
npm install

# Build application
npm run build

# Set environment variables
echo "NODE_ENV=production" > .env
echo "DATABASE_URL=postgresql://nmea_user:secure_password_here@localhost:5432/nmea_simulator" >> .env

# Start with PM2
pm2 start dist/index.js --name nmea-simulator
pm2 startup
pm2 save
```

### Step 4: Firewall Configuration

```bash
# Allow necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw allow 10110 # NMEA TCP
sudo ufw allow 4001  # Additional NMEA TCP
sudo ufw enable
```

### Step 5: Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt install nginx -y

# Create site configuration
sudo nano /etc/nginx/sites-available/nmea-simulator
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support for Signal K
    location /signalk/ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/nmea-simulator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 5000 10110 4001

CMD ["npm", "start"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
      - "10110:10110"
      - "4001:4001"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/nmea_simulator
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=nmea_simulator
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Deploy with:

```bash
docker-compose up -d
```

## Testing Connectivity

After deployment, test the connections:

### NMEA TCP Connection
```bash
# Test TCP connection (replace with your server IP)
telnet your-server-ip 10110
```

### Signal K WebSocket
```bash
# Test WebSocket connection
wscat -c ws://your-server-ip:5000/signalk/v1/stream
```

### HTTP Endpoints
```bash
# Test HTTP API
curl http://your-server-ip:5000/api/nmea/status
curl http://your-server-ip:5000/nmea.txt
```

## OpenCPN Configuration for Deployed Server

Once deployed, configure OpenCPN with:

**TCP Connection:**
- Protocol: TCP
- Address: `your-server-ip` or `your-domain.com`
- Port: `10110` or `4001`

**Signal K Connection:**
- WebSocket URL: `ws://your-domain.com/signalk/v1/stream`
- REST API: `http://your-domain.com/signalk/v1/api`

## Monitoring and Maintenance

```bash
# Check application status
pm2 status
pm2 logs nmea-simulator

# Check system resources
htop
df -h

# Update application
git pull
npm install
npm run build
pm2 restart nmea-simulator
```

## Recommended: Railway Quick Deploy

For the fastest deployment with minimal setup:

1. Go to railway.app
2. Click "Deploy from GitHub"
3. Connect your repository
4. Add PostgreSQL database
5. Deploy

Railway automatically handles:
- SSL certificates
- Domain management
- Environment variables
- Database connection
- Port forwarding

Your NMEA simulator will be accessible at `https://your-app.railway.app` with all TCP ports properly exposed for navigation apps.