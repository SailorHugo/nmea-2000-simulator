#!/bin/bash

# NMEA 2000 Simulator - GitHub Setup Script
# This script initializes a Git repository and prepares for GitHub upload

echo "Setting up NMEA 2000 Simulator for GitHub..."

# Initialize Git repository
git init

# Add .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production builds
dist/
build/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite
*.sqlite3

# NMEA output files
nmea_output.txt
*.nmea

# Logs
logs/
*.log

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
Thumbs.db

# Replit specific
.replit
replit.nix
EOF
fi

# Add all files to Git
echo "Adding files to Git..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: NMEA 2000 Simulator with Device Wizard

Features:
- Real-time marine data simulation
- 8 authentic device profiles (Garmin, Simrad, Airmar, Yanmar, etc.)
- One-click device configuration wizard
- Multiple NMEA output formats (TCP, WebSocket, Signal K)
- Ready for Railway deployment with proper TCP connectivity"

echo ""
echo "Git repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Create a repository on GitHub named 'nmea-2000-simulator'"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/nmea-2000-simulator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Railway:"
echo "   - Go to railway.app"
echo "   - Click 'Deploy from GitHub'"
echo "   - Select your repository"
echo "   - Add PostgreSQL database"
echo ""