# Marine Navigation App Connection Setup

## Signal K Connection (Recommended for Modern Apps)

### For OpenCPN with Signal K Plugin
1. Install the Signal K plugin in OpenCPN
2. Configure Signal K connection:
   - **Server URL**: `wss://dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev/signalk/v1/stream`
   - **REST API**: `https://dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev/signalk/v1/api`
   - **Protocol**: WebSocket Secure (WSS)
   - **Port**: 443 (HTTPS)

### For Other Signal K Compatible Apps
- **WebSocket Stream**: `wss://dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev/signalk/v1/stream`
- **HTTP API**: `https://dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev/signalk/v1/api`

### Available Signal K Data Paths
- `navigation.headingTrue` - Vessel heading in radians
- `navigation.speedOverGround` - Speed over ground in m/s
- `navigation.speedThroughWater` - Speed through water in m/s
- `navigation.position` - GPS coordinates in radians
- `environment.depth.belowKeel` - Water depth in meters
- `environment.wind.speedTrue` - Wind speed in m/s
- `environment.wind.directionTrue` - Wind direction in radians

## NMEA 0183 Connection (Traditional Method)

### Method 1: File Input (Most Reliable)

### Step 1: Download NMEA File
1. Open your web browser
2. Go to: `https://dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev/nmea.txt`
3. Right-click and "Save As" to your computer (e.g., Desktop/nmea.txt)
4. The file contains live NMEA data that updates every second

### Step 2: Configure OpenCPN File Input
1. Open OpenCPN
2. Go to **Options** → **Connections**
3. Click **Add Connection**
4. **Data Source**: Select "File"
5. **File Path**: Browse and select the downloaded nmea.txt file
6. **Priority**: Set to 1
7. **Control Checksum**: Check this box
8. **Receive Input on this Port**: Check this box
9. Click **Apply**

## Method 2: HTTP Data Source (Alternative)

### Step 1: Open OpenCPN Connection Settings
1. Open OpenCPN
2. Go to **Options** → **Connections**
3. Click **Add Connection**

### Step 2: Configure HTTP Data Source
1. **Data Source**: Select "Network"
2. **Protocol**: Select "TCP"
3. **Address**: Enter `dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev`
4. **DataPort**: Enter `80`
5. **Priority**: Set to 1
6. **Control Checksum**: Check this box
7. **Receive Input on this Port**: Check this box
8. **Output on this port**: Uncheck this box

### Step 3: Advanced Settings
1. **User Comment**: Enter "NMEA 2000 Simulator"
2. **Talker ID**: Leave as "Automatic"
3. **Connection Type**: "Serial/Network"
4. **Baudrate**: Not applicable for network connection
5. **Protocol**: "NMEA 0183"
6. **Discovery**: Uncheck

### Step 4: Apply and Test
1. Click **Apply**
2. The connection should show as "Connected" with a green indicator
3. You should start seeing data in the **NMEA Debug Window**

## Method 2: Alternative Network Setup

If Method 1 doesn't work, try:

### TCP Network Connection
1. **Protocol**: TCP
2. **Network Address**: `dc4c2421-7889-4528-98b5-96ddd295085b-00-efd6z3cgxueq.worf.replit.dev`
3. **Network Port**: `80`
4. **Connection Path**: `/nmea` (if supported by your OpenCPN version)

## Expected NMEA Data

You should see these sentence types in OpenCPN:
- **$GPHDG** - Heading (compass direction)
- **$GPVHW** - Speed through water
- **$GPDPT** - Water depth
- **$GPMWV** - Wind speed and direction
- **$GPROT** - Rate of turn
- **$GPTXT** - Status messages

## Troubleshooting

### Connection Issues
1. **Check Internet Connection**: Ensure OpenCPN can access the internet
2. **Firewall Settings**: Make sure your firewall allows OpenCPN to make HTTP connections
3. **OpenCPN Version**: Use OpenCPN 5.0 or newer for best network support

### Data Not Appearing
1. **Enable NMEA Debug**: Go to Options → User Interface → Show NMEA Debug Window
2. **Check Filters**: Ensure sentence filters aren't blocking the data
3. **Verify Connection Status**: Look for green "Connected" indicator

### Alternative Connection Methods
If network connection fails, you can try:
1. **File Input**: Save NMEA data to a file and use file input
2. **Virtual Serial Port**: Use software to create virtual COM ports (Windows only)

## Testing the Connection

1. Open **NMEA Debug Window** in OpenCPN
2. You should see sentences like:
   ```
   $GPHDG,180.5,,,,*52
   $GPVHW,,T,,M,6.2,N,11.5,K*73
   $GPDPT,25.3,0.0,*4F
   ```
3. The vessel position should update on the chart (if GPS simulation is enabled)
4. Instrument displays should show heading, speed, and depth values

## Data Rates
- Update frequency: 1 second
- Sentence types: 5 different NMEA sentences per update
- Data format: Standard NMEA 0183 with proper checksums

## Support
If you continue having issues:
1. Check OpenCPN forums for network connection troubleshooting
2. Verify the simulator URL is accessible in a web browser
3. Try different network protocols (TCP vs UDP) if available