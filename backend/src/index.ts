import express from 'express';
import cors from 'cors';
import config from './config';
import { connectDB } from './config/db';
import { securityHeaders, limiter } from './middleware/security';
import { globalErrorHandler, notFoundHandler } from './middleware/errorHandler';
import authRoutes from './routes/auth';
import conversationRoutes from './routes/conversations';
import bookmarkRoutes from './routes/bookmarks';
import healthRoutes from './routes/health';

// Initialize Express app
const app = express();

// Apply security middleware
app.use(securityHeaders);
app.use(limiter);

// Enable CORS with specific origins from config
const corsOptions = {
  origin: config.allowedOrigins,
  credentials: true,

  optionsSuccessStatus: 200,
};
app.use(cors(corsOptions));

// Parse JSON bodies
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check route (public)
app.use('/api/health', healthRoutes);

// Public routes
app.use('/api/auth', authRoutes);

// Protected routes
app.use('/api/conversations', conversationRoutes);
app.use('/api/bookmarks', bookmarkRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({ message: 'AI Textbook Backend API', version: '1.0.0' });
});

// 404 handler - should be after all routes
app.use((req, res, next) => {
  const error = new Error(`Route not found: ${req.originalUrl}`);
  (error as any).status = 404;
  next(error);
});

// Error handling middleware - should be last
app.use(globalErrorHandler);

// Connect to database and start server
connectDB().then(() => {
  app.listen(config.port, () => {
    console.log(`Backend server listening at http://localhost:${config.port}`);
    console.log(`Environment: ${config.nodeEnv}`);
  });
});

// Export app for testing
export default app;
