FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
COPY tsconfig.json ./
COPY .env ./

# Create logs directory
RUN mkdir -p logs

# Build the application
RUN npm run build

# Expose port
EXPOSE 3001

# Start the application
CMD [ "npm", "start:prod" ]