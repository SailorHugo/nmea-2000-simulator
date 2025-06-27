#!/usr/bin/env node

import { build } from 'esbuild';
import { execSync } from 'child_process';
import fs from 'fs';

console.log('Building for deployment...');

// Build frontend with Vite
console.log('Building frontend...');
execSync('npx vite build', { stdio: 'inherit' });

// Build backend with esbuild
console.log('Building backend...');
await build({
  entryPoints: ['server/index.ts'],
  bundle: true,
  format: 'esm',
  platform: 'node',
  outdir: 'dist',
  external: [
    'serialport',
    '@serialport/parser-readline',
    '@neondatabase/serverless'
  ],
  packages: 'external'
});

// Copy package.json for deployment
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const deployPkg = {
  name: pkg.name,
  version: pkg.version,
  type: 'module',
  scripts: {
    start: 'node index.js'
  },
  dependencies: {
    '@neondatabase/serverless': pkg.dependencies['@neondatabase/serverless'],
    'express': pkg.dependencies.express,
    'ws': pkg.dependencies.ws,
    'csv-writer': pkg.dependencies['csv-writer'],
    'drizzle-orm': pkg.dependencies['drizzle-orm'],
    'drizzle-zod': pkg.dependencies['drizzle-zod'],
    'zod': pkg.dependencies.zod,
    'serialport': pkg.dependencies.serialport,
    '@serialport/parser-readline': pkg.dependencies['@serialport/parser-readline']
  },
  engines: {
    node: '>=18.0.0'
  }
};

fs.writeFileSync('dist/package.json', JSON.stringify(deployPkg, null, 2));

console.log('Build complete! Ready for deployment.');