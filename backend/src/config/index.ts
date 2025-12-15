import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Configuration interface
interface Config {
  port: number;
  nodeEnv: string;
  googleApiKey: string;
  mongoUri: string;
  jwtSecret: string;
  jwtExpiresIn: string;
  rateLimitWindowMs: number;
  rateLimitMaxRequests: number;
  allowedOrigins: string[];
}

// Helper function to validate required environment variables
function getEnvVar(name: string, defaultValue?: string): string {
  const value = process.env[name];

  if (value === undefined) {
    if (defaultValue !== undefined) {
      return defaultValue;
    }
    throw new Error(`Environment variable ${name} is required but not set`);
  }

  return value;
}

// Helper function to parse array from comma-separated string
function parseArray(value: string): string[] {
  return value.split(',').map(item => item.trim()).filter(item => item.length > 0);
}

// Create and validate configuration
const config: Config = {
  port: parseInt(getEnvVar('PORT', '3001'), 10),
  nodeEnv: getEnvVar('NODE_ENV', 'development'),
  googleApiKey: getEnvVar('GOOGLE_API_KEY', ''),
  mongoUri: getEnvVar('MONGODB_URI', 'mongodb://localhost:27017/ai-book'),
  jwtSecret: getEnvVar('JWT_SECRET'),
  jwtExpiresIn: getEnvVar('JWT_EXPIRES_IN', '7d'),
  rateLimitWindowMs: parseInt(getEnvVar('RATE_LIMIT_WINDOW_MS', '900000'), 10), // 15 minutes default
  rateLimitMaxRequests: parseInt(getEnvVar('RATE_LIMIT_MAX_REQUESTS', '100'), 10),
  allowedOrigins: parseArray(getEnvVar('ALLOWED_ORIGINS', 'http://localhost:3000')),
};

// Validate port number
if (isNaN(config.port) || config.port < 1 || config.port > 65535) {
  throw new Error(`Invalid port number: ${config.port}`);
}

// Validate JWT expiration format (should be like '7d', '24h', etc.)
const jwtExpiryRegex = /^[1-9][0-9]*(s|m|h|d|w)$/;
if (!jwtExpiryRegex.test(config.jwtExpiresIn)) {
  throw new Error(`Invalid JWT expiration format: ${config.jwtExpiresIn}. Expected format: e.g., '7d', '24h', '30m'`);
}

// Validate rate limit values
if (config.rateLimitMaxRequests <= 0) {
  throw new Error(`Rate limit max requests must be positive, got: ${config.rateLimitMaxRequests}`);
}

if (config.rateLimitWindowMs <= 0) {
  throw new Error(`Rate limit window must be positive, got: ${config.rateLimitWindowMs}`);
}

export default config;