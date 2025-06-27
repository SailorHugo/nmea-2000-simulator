# Getting Your NMEA Simulator to GitHub

## Method 1: Download and Upload (Easiest)

### Step 1: Download Your Code
1. In Replit, click the **three dots menu** (⋯) in the file explorer
2. Select **Download as zip**
3. Save the zip file to your computer
4. Extract the zip file to a folder

### Step 2: Create GitHub Repository
1. Go to github.com and sign in (create account if needed)
2. Click the **green "New" button** or go to github.com/new
3. Repository name: `nmea-2000-simulator`
4. Description: `NMEA 2000 Marine Data Simulator with Signal K support`
5. Set to **Public** (required for free deployments)
6. Check **"Add a README file"**
7. Click **"Create repository"**

### Step 3: Upload Your Code
1. In your new GitHub repository, click **"uploading an existing file"**
2. Drag and drop all files from your extracted folder
3. **Important files to include:**
   - All `.ts`, `.tsx`, `.js` files
   - `package.json` and `package-lock.json`
   - `DEPLOYMENT_GUIDE.md`
   - `Dockerfile` and `docker-compose.yml`
   - `railway.json` and `render.yaml`
   - All folders: `client/`, `server/`, `shared/`
4. Write commit message: "Initial commit - NMEA 2000 Simulator"
5. Click **"Commit changes"**

## Method 2: Git Commands (Advanced)

If you're comfortable with Git:

### Step 1: Initialize Git in Replit
```bash
# In Replit shell
git init
git add .
git commit -m "Initial commit - NMEA 2000 Simulator"
```

### Step 2: Connect to GitHub
```bash
# Replace with your GitHub username and repository name
git remote add origin https://github.com/YOUR_USERNAME/nmea-2000-simulator.git
git branch -M main
git push -u origin main
```

## Essential Files for Deployment

Make sure these files are in your GitHub repository:

### Core Application Files
- `package.json` - Dependencies and scripts
- `server/` folder - All backend code
- `client/` folder - All frontend code  
- `shared/` folder - Shared types and schemas

### Deployment Configuration Files
- `Dockerfile` - For container deployment
- `docker-compose.yml` - For Docker Compose
- `railway.json` - Railway platform config
- `render.yaml` - Render platform config
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions

### Important: Update package.json

Create a new `package.json` for production with these scripts:

```json
{
  "name": "nmea-2000-simulator",
  "version": "1.0.0",
  "scripts": {
    "start": "node dist/index.js",
    "build": "npm run build:client && npm run build:server",
    "build:client": "vite build",
    "build:server": "esbuild server/index.ts --bundle --platform=node --target=node20 --outfile=dist/index.js --external:pg-native"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

## After Upload: Quick Deploy Options

### Option 1: Railway (Recommended)
1. Go to railway.app
2. Click **"Deploy from GitHub"**
3. Connect your repository
4. Add PostgreSQL database
5. Deploy automatically

### Option 2: Render
1. Go to render.com
2. Click **"New Web Service"**
3. Connect your GitHub repository
4. Select the repository
5. Auto-deploy starts

### Option 3: DigitalOcean
1. Go to cloud.digitalocean.com
2. Apps → Create App
3. Connect GitHub repository
4. Add managed database
5. Deploy

## Repository Structure

Your GitHub repository should look like this:

```
nmea-2000-simulator/
├── client/
│   ├── src/
│   ├── index.html
│   └── package.json
├── server/
│   ├── services/
│   ├── index.ts
│   └── routes.ts
├── shared/
│   └── schema.ts
├── package.json
├── Dockerfile
├── docker-compose.yml
├── railway.json
├── render.yaml
├── DEPLOYMENT_GUIDE.md
└── README.md
```

## Next Steps After GitHub Upload

1. **Choose deployment platform** (Railway recommended)
2. **Connect GitHub repository** to platform
3. **Add PostgreSQL database** 
4. **Set environment variables** (`NODE_ENV=production`)
5. **Deploy and test** TCP connections
6. **Configure your navigation app** with new server address

## Troubleshooting

### If files are missing:
- Re-download from Replit
- Check all folders are included
- Verify package.json has correct scripts

### If deployment fails:
- Check build logs in platform dashboard
- Ensure all dependencies are in package.json
- Verify Node.js version is 20 or higher

### If TCP connections don't work:
- Confirm platform supports custom ports
- Check firewall settings
- Test with telnet: `telnet your-domain.com 10110`

## Railway Deployment Fix

If you get a "monorepo without correct root directory" error on Railway:

### Method 1: Upload Required Files
Make sure these files are in your GitHub repository root:
- `package.json` - Main project configuration
- `railway.json` - Railway deployment config  
- `nixpacks.toml` - Build system configuration

### Method 2: Manual Railway Configuration
1. In Railway dashboard, go to your service settings
2. Under "Build & Deploy", set:
   - **Root Directory**: `/` (leave empty)
   - **Build Command**: `npm run build`
   - **Start Command**: `npm start`
3. Add environment variable: `NODE_ENV=production`

### Method 3: Fresh Deployment
If Railway still shows the error:
1. Delete the service from Railway
2. Create a new service
3. Select "Deploy from GitHub repo"
4. Choose your repository again
5. Railway should detect it as a Node.js app

Once your code is on GitHub, deployment to platforms with proper TCP support takes just a few minutes!