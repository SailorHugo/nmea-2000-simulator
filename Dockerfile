FROM node:20-alpine

# Install system dependencies
RUN apk add --no-cache git

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application using working build script
RUN chmod +x simple-build.sh && ./simple-build.sh

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nmea -u 1001

# Change ownership
RUN chown -R nmea:nodejs /app
USER nmea

# Expose ports
EXPOSE 5000 10110 4001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/pgn-configurations || exit 1

# Install production dependencies and start
WORKDIR /app/dist
RUN npm install --production
CMD ["npm", "start"]