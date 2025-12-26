import { betterAuth } from "better-auth";
import Database from "better-sqlite3";

// Initialize SQLite database
const db = new Database("./better_auth.db");

// Create Better Auth instance with custom schema
export const auth = betterAuth({
  database: {
    provider: "sqlite",
    client: db,
  },
  // Add custom fields to the user model
  user: {
    additionalFields: {
      software_experience: {
        type: "string",
        required: false,
      },
      hardware_knowledge: {
        type: "string",
        required: false,
      },
      interests: {
        type: "string", // Store as JSON string
        required: false,
      },
    },
  },
  // Authentication options
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  // Session options
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["email-password"], // Only email-password linking
    },
  },
  // API configuration
  api: {
    baseURL: process.env.AUTH_BASE_URL || "http://localhost:8002",
    baseEndpoint: "/api/auth/better", // Custom endpoint prefix
  },
  // Security options
  secret: process.env.AUTH_SECRET || "your-super-secret-jwt-key-change-in-production",
  // Rate limiting
  rateLimit: {
    window: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per window
  },
  // Email configuration
  email: {
    enabled: true,
    from: process.env.AUTH_EMAIL_FROM || "noreply@localhost",
  },
});

