# Railway Deployment Guide

## Step-by-Step Railway Deployment

### 1. Prepare Repository
Ensure your repository has these files in the root:
- ✅ `package.json`
- ✅ `railway.json`  
- ✅ `replit.md`

### 2. Deploy to Railway

**Option A: GitHub Connection (Recommended)**
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your NMEA simulator repository
6. Railway will automatically detect and deploy

**Option B: CLI Deployment**
```bash
npm install -g @railway/cli
railway login
railway deploy
```

### 3. Add Database
1. In your Railway project dashboard
2. Click "Add Service"
3. Select "PostgreSQL"
4. Railway automatically connects `DATABASE_URL`

### 4. Configure Environment
Railway automatically provides:
- `PORT` (usually 8080 or dynamic)
- `DATABASE_URL` (from PostgreSQL service)
- `RAILWAY_ENVIRONMENT=production`

### 5. Verify Deployment
1. Railway provides a public URL (e.g., `yourapp.railway.app`)
2. Visit the URL to see your simulator
3. Check that database connections work

## Common Railway Issues & Solutions

### Build Fails
**Check these in Railway logs:**
```
npm install && npm run build
```

**If serialport issues:**
Railway uses Linux containers, so native modules should build correctly.

### Database Not Connecting
**Verify in Railway dashboard:**
1. PostgreSQL service is running
2. `DATABASE_URL` environment variable exists
3. No firewall issues (Railway handles this)

### Application Not Starting
**Check start command:**
```json
{
  "deploy": {
    "startCommand": "npm start"
  }
}
```

**Verify package.json:**
```json
{
  "scripts": {
    "start": "NODE_ENV=production node dist/index.js"
  }
}
```

## Expected Timeline
- Repository connection: 1 minute
- Initial build: 3-5 minutes
- Database setup: 1 minute
- **Total deployment time: 5-7 minutes**

## Railway Advantages
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ✅ Built-in PostgreSQL
- ✅ TCP port support (for NMEA connections)
- ✅ Automatic scaling
- ✅ Free tier available

## After Successful Deployment

Your NMEA simulator will be available at:
- Web interface: `https://yourapp.railway.app`
- NMEA TCP: `yourapp.railway.app:10110`
- Signal K: `wss://yourapp.railway.app/signalk/v1/stream`

## Cost Estimation
- **Free tier:** 500 hours/month (sufficient for testing)
- **Pro plan:** $5/month (unlimited usage)
- **Database:** $5/month (included in Pro plan)

Railway is the recommended platform for this NMEA simulator because it provides full TCP port support needed for navigation apps like OpenCPN.