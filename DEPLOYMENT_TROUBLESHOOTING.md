# Deployment Troubleshooting Guide

## Common Railway Deployment Issues

### 1. "No package.json found" Error
**Solution:**
- Ensure `package.json` is in the repository root
- Check that files are properly committed to Git
- Verify Railway is pointing to correct repository branch

### 2. Build Timeout or Memory Issues
**Solution:**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm ci --only=production && npm run build"
  }
}
```

### 3. Database Connection Issues
**Railway Setup:**
1. Add PostgreSQL plugin to your Railway project
2. Railway automatically provides `DATABASE_URL`
3. No additional configuration needed

### 4. Port Configuration
Railway automatically assigns `PORT` environment variable. Our app uses:
```javascript
const port = process.env.PORT || 5000;
```

## Common Render Deployment Issues

### 1. Build Command Fails
**Render Settings:**
- Build Command: `npm install && npm run build`
- Start Command: `npm start`
- Node Version: 20

### 2. Database Setup
**Render Dashboard:**
1. Create PostgreSQL database
2. Copy connection string
3. Add as `DATABASE_URL` environment variable

### 3. Custom Ports for NMEA
**Important:** Render's free tier only supports HTTP/HTTPS. For TCP connections:
- Upgrade to paid plan ($7/month minimum)
- Configure additional ports in render.yaml

## Quick Deployment Steps

### Railway (Recommended)
1. Push code to GitHub
2. Connect Railway to repository
3. Add PostgreSQL database
4. Deploy automatically

### Render Alternative
1. Fork repository to GitHub
2. Connect Render to repository
3. Create PostgreSQL database
4. Set environment variables
5. Deploy

## Verified Working Configuration

The current repository includes:
- ✅ Correct package.json scripts
- ✅ Railway configuration (railway.json)
- ✅ Render configuration (render.yaml)
- ✅ Production build settings
- ✅ Database schema and migrations

## Environment Variables Required

```
NODE_ENV=production
DATABASE_URL=postgresql://username:password@host:port/database
PORT=5000 (auto-provided by hosting platforms)
```

## Health Check Endpoints

Both platforms check: `/api/pgn-configurations`
This endpoint returns JSON status confirming the app is running.

## If Deployment Still Fails

1. **Check Repository Structure:**
   ```
   ├── package.json (must be in root)
   ├── railway.json
   ├── render.yaml
   ├── client/
   ├── server/
   └── shared/
   ```

2. **Verify Dependencies:**
   - All dependencies in package.json
   - No missing imports
   - Proper build script

3. **Platform-Specific:**
   - **Railway:** Check build logs in dashboard
   - **Render:** Verify environment variables are set

## Test Local Production Build

Before deploying, test locally:
```bash
npm run build
npm start
```

Visit `http://localhost:5000` to verify the production build works.