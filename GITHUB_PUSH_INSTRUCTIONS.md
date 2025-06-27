# Push NMEA Simulator to GitHub

Since you can't download the files, here's how to push directly from Replit:

## Method 1: Using Replit's GitHub Integration

1. **In Replit Console** (click Shell tab at bottom):
   ```bash
   # Add your changes
   git add .
   
   # Commit with description
   git commit -m "Add Device Wizard feature with 8 marine devices"
   ```

2. **Create GitHub Repository**:
   - Go to github.com
   - Click "New repository"
   - Name: `nmea-2000-simulator`
   - Make it Public
   - DON'T initialize with README (we already have one)

3. **Connect and Push**:
   ```bash
   # Replace YOUR_USERNAME with your GitHub username
   git remote add origin https://github.com/YOUR_USERNAME/nmea-2000-simulator.git
   git branch -M main
   git push -u origin main
   ```

   Note: You'll need to provide your GitHub username and password/token when prompted.

## Method 2: Manual File Upload

If Git doesn't work, create the repository and manually copy these key files:

### Essential Files to Copy:
1. **package.json** - Main project configuration
2. **README.md** - Project documentation
3. **railway.json** - Railway deployment config
4. **nixpacks.toml** - Build configuration
5. **Dockerfile** - Container setup
6. **DEPLOYMENT_GUIDE.md** - Complete deployment instructions

### Copy Directory Structure:
```
nmea-2000-simulator/
├── client/src/components/device-wizard.tsx
├── client/src/pages/simulator.tsx
├── server/routes.ts
├── shared/schema.ts
└── (all other files)
```

## After GitHub Upload:

### Deploy to Railway:
1. Go to railway.app
2. Click "Deploy from GitHub"
3. Select your `nmea-2000-simulator` repository
4. Add PostgreSQL database
5. Deploy

### Railway will automatically:
- Use nixpacks.toml for Node.js detection
- Run npm install and npm run build
- Start with npm start
- Expose ports 5000, 10110, 4001 for TCP connections

## Testing OpenCPN Connection:
Once deployed, configure OpenCPN:
- **TCP Host**: your-app.railway.app
- **Port**: 10110 or 4001
- **Protocol**: TCP

Your simulator includes authentic data from 8 real marine devices and will work properly with external navigation software once deployed.