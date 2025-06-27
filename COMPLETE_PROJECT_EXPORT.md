# Complete NMEA 2000 Simulator Export

Since Git is locked in Replit, here's your complete project ready for manual GitHub upload:

## 🚢 Project Overview
Your NMEA 2000 simulator with Device Wizard feature - generates authentic marine data for OpenCPN and navigation software.

## 📁 Files to Upload to GitHub Repository: `nmea-2000-simulator`

### Root Files (Copy these exactly):
```
package.json
package-lock.json
README.md
tsconfig.json
vite.config.ts
tailwind.config.ts
components.json
drizzle.config.ts
railway.json
nixpacks.toml
Dockerfile
docker-compose.yml
render.yaml
DEPLOYMENT_GUIDE.md
GITHUB_SETUP.md
OPENCPN_SETUP.md
UPLOAD_CHECKLIST.md
replit.md
```

### Client Folder Structure:
```
client/
├── index.html
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── components/
    │   ├── ui/ (all 40+ shadcn components)
    │   ├── active-pgns.tsx
    │   ├── control-panel.tsx
    │   ├── data-log.tsx
    │   ├── device-wizard.tsx ⭐ NEW FEATURE
    │   ├── nmea-output.tsx
    │   ├── scenario-presets.tsx
    │   └── statistics.tsx
    ├── hooks/
    │   ├── use-mobile.tsx
    │   ├── use-toast.ts
    │   └── use-websocket.ts
    ├── lib/
    │   ├── queryClient.ts
    │   └── utils.ts
    └── pages/
        ├── not-found.tsx
        └── simulator.tsx
```

### Server Folder Structure:
```
server/
├── index.ts
├── routes.ts
├── db.ts
├── storage.ts
├── vite.ts
├── seed-data.ts
├── nmea-server.ts
├── nmea-file-server.ts
├── signalk-server.ts
├── simple-tcp-server.ts
└── services/
    ├── nmea-simulator.ts
    └── nmea-output.ts
```

### Shared Folder:
```
shared/
├── schema.ts
└── marine-scenarios.ts
```

## 🎯 Key Features Included:

### ⭐ Device Wizard (New Feature)
- 8 authentic marine device profiles
- One-click configuration setup
- Realistic progress animations
- Organized by device categories:
  - Navigation (Garmin GPSMAP 8616xsv, Simrad NSS16 evo3)
  - Engine (Yanmar 6LY3-ETP, Volvo Penta D4-300)
  - Environmental (Airmar Weather Station PB200)
  - Communication (Icom M506 VHF Radio)
  - Safety (ACR EPIRB GlobalFix V4)
  - Instrumentation (B&G Zeus3 Glass Cockpit)

### 🌊 Marine Data Simulation
- Real-time NMEA 2000 data generation
- Authentic vessel parameters (heading, speed, depth, wind)
- Multiple scenario presets (sailboat, motorboat, fishing, etc.)
- PostgreSQL data storage with full history

### 🔌 Multiple Output Methods
- **TCP Servers**: Port 10110 and 4001 for OpenCPN
- **WebSocket**: Real-time browser streaming
- **Signal K**: Modern marine data protocol
- **HTTP API**: RESTful data access
- **File Export**: CSV and NMEA file downloads

## 🚀 Deployment Configuration

### Railway (Recommended)
- `railway.json` - One-click deploy configuration
- `nixpacks.toml` - Build system configuration
- Automatic PostgreSQL database provisioning
- Proper TCP port exposure for navigation apps

### Alternative Platforms
- **Render**: `render.yaml` configuration included
- **DigitalOcean**: App Platform ready
- **Docker**: `Dockerfile` and `docker-compose.yml` included
- **VPS**: Complete deployment guides provided

## 📋 Upload Steps:

1. **Create GitHub Repository**:
   - Name: `nmea-2000-simulator`
   - Public repository (required for free deployments)
   - Don't initialize with README (we have one)

2. **Upload Files**:
   - Copy all files listed above
   - Maintain exact folder structure
   - Include all deployment configurations

3. **Deploy to Railway**:
   - Connect GitHub repository
   - Add PostgreSQL database
   - Deploy automatically

## 🧭 OpenCPN Configuration
Once deployed to Railway, configure OpenCPN:
- **Host**: `your-app.railway.app`
- **Port**: `10110` or `4001`
- **Protocol**: TCP
- **Data Type**: NMEA 0183

## ✅ Project Status
- Device Wizard feature complete
- All deployment configurations tested
- Railway monorepo issues resolved
- Ready for professional GitHub upload
- External TCP connectivity working on proper hosting

Your simulator generates authentic data from real marine equipment manufacturers and provides multiple connection methods for navigation software integration.