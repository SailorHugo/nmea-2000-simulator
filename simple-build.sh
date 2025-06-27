#!/bin/bash
set -e

echo "Building NMEA Simulator for deployment..."

# Build frontend quickly
echo "Building frontend..."
NODE_ENV=production npx vite build --minify false

# Build backend with minimal bundling
echo "Building backend..."
npx esbuild server/index.ts \
  --platform=node \
  --format=esm \
  --outdir=dist \
  --external:serialport \
  --external:@serialport/parser-readline \
  --external:@neondatabase/serverless \
  --external:drizzle-orm \
  --external:express \
  --external:ws \
  --packages=external \
  --bundle

echo "Build complete!"
echo "Frontend built to: dist/public"
echo "Backend built to: dist/index.js"