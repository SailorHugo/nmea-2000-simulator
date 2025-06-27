# GitHub Upload Checklist - NMEA 2000 Simulator

## Step 1: Download Your Code from Replit

1. In Replit, click the **three dots menu** (⋯) in the file explorer
2. Select **"Download as zip"**
3. Extract the zip file to a folder on your computer

## Step 2: Essential Files to Upload

### ✅ Core Application Files (REQUIRED)
- `client/` folder - Complete React frontend with Device Wizard
- `server/` folder - Complete Express backend with device endpoints
- `shared/` folder - Shared types and schemas
- `package.json` - Main dependencies and scripts
- `package-lock.json` - Exact dependency versions
- `tsconfig.json` - TypeScript configuration

### ✅ Deployment Configuration Files (REQUIRED)
- `railway.json` - Railway platform configuration
- `nixpacks.toml` - Build system configuration  
- `render.yaml` - Render platform configuration
- `Dockerfile` - Docker containerization
- `docker-compose.yml` - Docker Compose setup

### ✅ Documentation Files (REQUIRED)
- `README.md` - Project overview and setup
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions
- `GITHUB_SETUP.md` - GitHub upload guide
- `.gitignore` - Files to exclude from Git

### ✅ Build Configuration Files (REQUIRED)
- `vite.config.ts` - Frontend build configuration
- `tailwind.config.ts` - CSS framework setup
- `postcss.config.js` - CSS processing
- `components.json` - UI component configuration
- `drizzle.config.ts` - Database ORM configuration

### ❌ Files to EXCLUDE (Don't Upload)
- `node_modules/` folder - Dependencies (too large)
- `nmea_output.txt` - Generated file
- `.replit` - Replit-specific configuration
- `replit.nix` - Replit environment file
- Any `.env` files with sensitive data

## Step 3: Create GitHub Repository

1. Go to **github.com** and sign in
2. Click the **green "New" button**
3. Repository settings:
   - **Name**: `nmea-2000-simulator`
   - **Description**: `NMEA 2000 Marine Data Simulator with Signal K support`
   - **Visibility**: Public (required for free deployments)
   - **Initialize**: Check "Add a README file"
4. Click **"Create repository"**

## Step 4: Upload Files to GitHub

### Method A: Web Upload (Easiest)
1. In your new repository, click **"uploading an existing file"**
2. Drag and drop ALL files from your extracted folder
3. **Important**: Make sure these files are in the root directory:
   - `package.json`
   - `railway.json` 
   - `nixpacks.toml`
   - `README.md`
4. Commit message: `Initial commit - NMEA 2000 Simulator`
5. Click **"Commit changes"**

### Method B: Git Commands (Advanced)
```bash
# Navigate to your extracted folder
cd path/to/your/nmea-simulator

# Initialize Git
git init
git add .
git commit -m "Initial commit - NMEA 2000 Simulator"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nmea-2000-simulator.git
git branch -M main
git push -u origin main
```

## Step 5: Verify Upload Success

Check that your repository includes:
- ✅ All folders: `client/`, `server/`, `shared/`
- ✅ Root files: `package.json`, `railway.json`, `nixpacks.toml`
- ✅ Documentation: `README.md`, `DEPLOYMENT_GUIDE.md`
- ✅ No `node_modules/` folder

## Step 6: Deploy to Railway

1. Go to **railway.app**
2. Click **"Deploy from GitHub"**
3. Select your `nmea-2000-simulator` repository
4. Railway will automatically detect Node.js and use your configuration files
5. Add **PostgreSQL database** from Railway dashboard
6. Your app will build and deploy automatically

## Step 7: Test Your Deployment

Once deployed, test these endpoints:
- `https://your-app.railway.app` - Web interface
- `https://your-app.railway.app/api/nmea/status` - API status
- `https://your-app.railway.app/nmea.txt` - NMEA file download

## Railway Configuration (If Needed)

If Railway shows deployment errors, manually set:
- **Root Directory**: `/` (leave empty)
- **Build Command**: `npm run build`
- **Start Command**: `npm start`
- **Environment Variables**: `NODE_ENV=production`

## OpenCPN Connection

After successful deployment, configure OpenCPN:
- **TCP Connection**: `your-app.railway.app:10110`
- **Signal K**: `wss://your-app.railway.app/signalk/v1/stream`

## File Size Check

Your upload should be approximately:
- **Total size**: ~50-100 MB (without node_modules)
- **File count**: ~200-300 files
- **Folder structure**: 3 main folders (client, server, shared)

If your upload is larger than 200 MB, you likely included `node_modules/` by mistake.