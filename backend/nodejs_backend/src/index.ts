import express from "express";
import cors from "cors";
import { auth } from "../auth/better-auth";
import "dotenv/config";

const app = express();
const PORT = parseInt(process.env.PORT || "8002");

// Middleware
app.use(cors({
  origin: [
    "http://localhost:3000", // Frontend
    "http://localhost:3001",
    "http://localhost:8000", // Existing backend
    process.env.FRONTEND_URL || ""
  ].filter(url => url !== ""), // Remove empty strings
  credentials: true,
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization", "Accept"],
}));

app.use(express.json());

// Mount Better Auth routes - using the handler function
app.use("/api/auth/better", async (req, res, next) => {
  try {
    // Create a Headers object from Express headers
    const headers = new Headers();
    for (const [key, value] of Object.entries(req.headers)) {
      if (value !== undefined) {
        headers.set(key, Array.isArray(value) ? value.join(', ') : value.toString());
      }
    }

    // Create a proper Request object for Better Auth
    const request = new Request(`http://localhost:${PORT}${req.url}`, {
      method: req.method,
      headers,
      body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
    });

    // Call the Better Auth handler with the Request object
    const response = await auth.handler(request);

    // Set the response headers
    for (const [key, value] of response.headers.entries()) {
      res.setHeader(key, value);
    }

    // Send the response
    res.status(response.status).send(await response.text());
  } catch (error) {
    console.error('Error in Better Auth handler:', error);
    next(error);
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Better Auth Service" });
});

// Root endpoint
app.get("/", (req, res) => {
  res.json({
    message: "Better Auth Service for Physical AI & Humanoid Robotics Textbook",
    endpoints: {
      auth: "/api/auth/better/*",
      health: "/health"
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Better Auth Service running on port ${PORT}`);
  console.log(`API available at: http://localhost:${PORT}/api/auth/better`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

export default app;