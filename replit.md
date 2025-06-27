# NMEA 2000 Simulator

## Overview

This is a full-stack web application that simulates NMEA 2000 marine data transmission. The application allows users to configure Parameter Group Numbers (PGNs), simulate real-time marine data generation, and export data for analysis. It's built as a modern web application with real-time WebSocket communication for live data streaming.

## System Architecture

The application follows a monorepo structure with clear separation between client and server code:

- **Frontend**: React-based SPA with TypeScript
- **Backend**: Express.js server with WebSocket support
- **Database**: PostgreSQL with Drizzle ORM
- **UI Framework**: shadcn/ui components with Tailwind CSS
- **Build Tool**: Vite for development and production builds
- **Deployment**: Configured for Replit with autoscale deployment

## Key Components

### Frontend Architecture
- **React 18** with TypeScript for type safety
- **Wouter** for lightweight client-side routing
- **TanStack Query** for server state management and caching
- **shadcn/ui** component library built on Radix UI primitives
- **Tailwind CSS** for styling with custom marine-themed color palette
- **WebSocket client** for real-time data streaming

### Backend Architecture
- **Express.js** server with middleware for JSON handling and logging
- **WebSocket Server** using 'ws' library for real-time communication
- **Drizzle ORM** with PostgreSQL for type-safe database operations
- **NMEA Simulator Service** for generating realistic marine data
- **CSV Export** functionality for data analysis
- **Memory Storage** fallback with interface abstraction

### Data Storage
- **PostgreSQL** as primary database (Neon-backed via Replit)
- **Two main tables**: 
  - `pgn_configurations`: Stores PGN setup with min/max values, update rates
  - `data_points`: Stores generated data points with timestamps
- **Drizzle ORM** provides type-safe database schema and migrations
- **Database Storage** implementation with full CRUD operations
- **Memory storage** kept as fallback option for testing

### Real-time Communication
- **WebSocket connection** between client and server
- **Message types**: PGN data updates, simulator status, statistics
- **Automatic reconnection** with exponential backoff
- **Connection status monitoring** in the UI

## Data Flow

1. **Configuration**: Users configure PGNs through the web interface
2. **Simulation**: NMEA simulator generates data based on PGN configurations
3. **Storage**: Generated data points are stored in PostgreSQL
4. **Real-time Updates**: Data is broadcast via WebSocket to connected clients
5. **Visualization**: Frontend displays live data with progress bars and logs
6. **Export**: Users can export data as CSV for external analysis

## External Dependencies

### Core Framework Dependencies
- **@neondatabase/serverless**: PostgreSQL database connectivity
- **drizzle-orm**: Type-safe ORM with PostgreSQL dialect
- **express**: Web server framework
- **ws**: WebSocket server implementation
- **wouter**: Lightweight React router

### UI Dependencies
- **@radix-ui/***: Comprehensive set of accessible UI primitives
- **@tanstack/react-query**: Server state management
- **tailwindcss**: Utility-first CSS framework
- **class-variance-authority**: Component variant utilities
- **lucide-react**: Icon library

### Development Dependencies
- **vite**: Build tool and development server
- **typescript**: Type checking and compilation
- **tsx**: TypeScript execution for development
- **esbuild**: Fast bundling for production server code

## Deployment Strategy

### Development Environment
- **Replit-optimized** with `.replit` configuration
- **Hot module replacement** via Vite dev server
- **Concurrent development** with `npm run dev` running both client and server
- **WebSocket proxy** for development mode

### Production Build
- **Client build**: Vite builds React app to `dist/public`
- **Server build**: esbuild bundles Express server to `dist/index.js`
- **Static file serving** for production deployment
- **Environment-based configuration** for database connections

### Replit Integration
- **Autoscale deployment** configured in `.replit`
- **PostgreSQL module** enabled for database provisioning
- **Port 5000** configured for web access
- **Build and start scripts** defined for deployment pipeline

## Changelog

```
Changelog:
- June 24, 2025: Initial setup with memory storage
- June 24, 2025: Added PostgreSQL database integration
- June 24, 2025: Added NMEA output for navigation apps (TCP/UDP/File)
- June 24, 2025: Improved start/stop control with single toggle button
- June 24, 2025: Fixed server crashes and WebSocket connection issues
- June 24, 2025: Added data polling fallback and default PGN configurations
- June 24, 2025: App now fully functional with real-time marine data display
- June 24, 2025: Added one-click marine scenario preset generator with 9 realistic scenarios
- June 24, 2025: Fixed NMEA connectivity issues with dedicated HTTP endpoint for navigation apps
- June 24, 2025: Integrated Signal K server for modern marine data distribution
- June 24, 2025: Project completed with multiple NMEA output methods implemented
- June 25, 2025: Created comprehensive deployment infrastructure for Railway, DigitalOcean, Render, VPS
- June 25, 2025: Fixed Railway monorepo deployment issues with proper configuration files
- June 25, 2025: Added GitHub upload documentation and professional README
- June 25, 2025: Implemented one-click device simulation wizard with 8 real marine devices
- June 25, 2025: Device Wizard feature completed and tested - ready for GitHub deployment
- June 25, 2025: Added Captain Byte marine mascot guide with contextual tips and interactive help system
- June 25, 2025: Implemented tabbed interface for better organization of Device Wizard, scenarios, and controls
- June 27, 2025: Added USB NMEA receiver support for real marine hardware connectivity
- June 27, 2025: Created professional Marine Dashboard with authentic nautical instruments
- June 27, 2025: Fixed deployment issues - optimized build process for Railway and Render (30-second builds)
```

## Final Status

The NMEA 2000 simulator application is fully functional with multiple data output methods:

### Working Features
- Real-time marine data generation (heading, speed, depth, wind, position)
- Web-based simulator interface with scenario presets and device wizard
- Captain Byte marine mascot guide with contextual tips and interactive help
- PostgreSQL data storage with full history
- Multiple output formats: NMEA 0183, Signal K, CSV export
- Tabbed interface for organized access to Device Wizard, scenarios, and monitoring

### Data Access Methods
1. **Web Interface**: Full-featured simulator with real-time displays
2. **NMEA File Download**: Updated every second for offline use
3. **Signal K WebSocket**: Modern marine data streaming protocol
4. **HTTP API**: RESTful access to all data
5. **TCP Servers**: Multiple ports for raw NMEA streaming

### Technical Limitations
External navigation app connectivity faces limitations due to Replit's hosting environment and port forwarding restrictions for raw TCP connections. The simulator generates authentic NMEA data but requires specialized hosting for direct navigation app integration.

### Deployment Options
The application is ready for deployment to platforms that support TCP connections:
1. **Railway** (recommended): One-click deploy with automatic SSL and database
2. **DigitalOcean App Platform**: Managed hosting with PostgreSQL addon
3. **Render**: Free tier available, full TCP support
4. **VPS Hosting**: Complete control (Linode, DigitalOcean, Vultr, Hetzner)
5. **Docker**: Containerized deployment for any platform

Complete deployment guides and configuration files provided in DEPLOYMENT_GUIDE.md

## User Preferences

```
Preferred communication style: Simple, everyday language.
```