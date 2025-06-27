# NMEA 2000 Simulator

A comprehensive marine data simulator that generates realistic NMEA 2000 data for testing navigation applications like OpenCPN. Features real-time data streaming via multiple protocols including NMEA 0183, Signal K, and WebSocket connections.

![NMEA Simulator](https://img.shields.io/badge/NMEA-2000%20Simulator-blue)
![Node.js](https://img.shields.io/badge/Node.js-20+-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)

## Features

### Real-time Marine Data Generation
- **Vessel Navigation**: Heading, speed over ground, speed through water
- **Environmental Data**: Water depth, wind speed and direction
- **Position Data**: GPS coordinates with realistic movement simulation
- **Rate of Turn**: Dynamic turning calculations

### Multiple Output Formats
- **NMEA 0183**: Standard marine data sentences with proper checksums
- **Signal K**: Modern JSON-based marine data protocol
- **WebSocket Streaming**: Real-time data push to connected clients
- **HTTP API**: RESTful access to all data endpoints
- **File Export**: CSV and NMEA text file downloads

### Marine Scenarios & Device Wizard
Pre-configured realistic scenarios including:
- **Vessel Types**: Sailboat, Motor Yacht, Commercial Vessel, Fishing Boat
- **Weather Conditions**: Calm, Rough Seas, Storm, Harbor
- **Activities**: Anchored, Racing, Fishing, Cruising, Docking

One-click device simulation wizard with authentic marine equipment:
- **Navigation**: Garmin GPSMAP 8424, Simrad RC42 Compass, Furuno DRS25A Radar
- **Engine**: Yanmar 6LY3-ETP with full electronic monitoring
- **Environmental**: Airmar 200WX WeatherStation
- **Communication**: Vesper Cortex M1 AIS Transponder

### Navigation App Support
- **OpenCPN**: Direct TCP and Signal K connections
- **Signal K Compatible Apps**: WebSocket and HTTP API
- **Any NMEA 0183 App**: Via TCP ports 10110 and 4001

## Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/nmea-2000-simulator.git
cd nmea-2000-simulator

# Install dependencies
npm install

# Start development server
npm run dev
```

### Docker Deployment
```bash
# Quick start with Docker Compose
docker-compose up -d
```

### Cloud Deployment

#### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Click "Deploy on Railway"
2. Connect GitHub repository
3. Add PostgreSQL database
4. Deploy automatically

#### Other Platforms
- **Render**: See `render.yaml` configuration
- **DigitalOcean**: App Platform with managed database
- **VPS**: Complete setup guide in `DEPLOYMENT_GUIDE.md`

## API Endpoints

### NMEA Data Access
- `GET /nmea.txt` - Download current NMEA file
- `GET /nmea/data` - Current NMEA sentences
- `GET /nmea` - HTTP streaming NMEA data
- `TCP :10110` - Raw NMEA TCP connection
- `TCP :4001` - Alternative NMEA TCP connection

### Signal K Protocol
- `WebSocket /signalk/v1/stream` - Real-time Signal K data
- `GET /signalk/v1/api` - Signal K REST API
- `GET /signalk/v1/api/vessels` - All vessel data

### Application API
- `GET /api/nmea/status` - Server status and statistics
- `GET /api/pgn-configurations` - PGN configuration list
- `GET /api/data-points` - Historical data points
- `POST /api/scenarios/apply` - Apply marine scenario

## Navigation App Configuration

### OpenCPN Setup

**Method 1: TCP Connection**
- Protocol: TCP
- Address: `your-server-domain.com`
- Port: `10110` or `4001`
- Enable "Receive Input" and "Control Checksum"

**Method 2: Signal K (with plugin)**
- WebSocket: `wss://your-server-domain.com/signalk/v1/stream`
- REST API: `https://your-server-domain.com/signalk/v1/api`

**Method 3: File Input**
- Download: `https://your-server-domain.com/nmea.txt`
- Configure OpenCPN to read from downloaded file

### Other Navigation Apps
Most modern marine navigation software supports either:
- Direct TCP NMEA connections (ports 10110, 4001)
- Signal K protocol (WebSocket or HTTP)
- NMEA file import

## Technology Stack

### Backend
- **Node.js 20+** with TypeScript
- **Express.js** for HTTP server
- **WebSocket (ws)** for real-time connections
- **PostgreSQL** with Drizzle ORM
- **Signal K** protocol implementation

### Frontend
- **React 18** with TypeScript
- **Vite** for development and building
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **TanStack Query** for data management

### Marine Protocols
- **NMEA 0183** sentence generation
- **Signal K** delta messages
- **PGN (Parameter Group Numbers)** simulation
- **Proper checksums** and validation

## Data Accuracy

The simulator generates realistic marine data with:
- **Authentic NMEA sentences**: HDG, VHW, DPT, MWV, ROT, GGA
- **Proper checksums**: All sentences include valid checksums
- **Realistic values**: Data ranges match real-world marine equipment
- **Temporal consistency**: Values change realistically over time
- **Navigation accuracy**: Position data suitable for chart plotting

## Development

### Project Structure
```
├── client/          # React frontend application
├── server/          # Express.js backend server
├── shared/          # Shared types and schemas
├── Dockerfile       # Container configuration
└── DEPLOYMENT_GUIDE.md  # Complete deployment instructions
```

### Environment Variables
```bash
NODE_ENV=production
DATABASE_URL=postgresql://user:password@host:port/database
```

### Database Schema
- **pgn_configurations**: PGN setup and parameters
- **data_points**: Generated data points with timestamps

### Building for Production
```bash
npm run build        # Build both client and server
npm start           # Start production server
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For deployment assistance or technical questions:
- Review `DEPLOYMENT_GUIDE.md` for detailed platform instructions
- Check `OPENCPN_SETUP.md` for navigation app configuration
- Open GitHub issue for bugs or feature requests

## Acknowledgments

- **NMEA 0183** standard for marine data communication
- **Signal K** project for modern marine data protocols
- **OpenCPN** community for navigation software excellence
- **Marine industry** for protocol specifications and testing feedback