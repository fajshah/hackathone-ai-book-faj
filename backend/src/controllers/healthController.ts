import { Request, Response } from 'express';
import mongoose from 'mongoose';

// Health check endpoint
export const healthCheck = async (req: Request, res: Response): Promise<void> => {
  try {
    // Check if MongoDB is connected
    const dbHealth = mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';

    // Basic response time measurement
    const startTime = Date.now();
    const responseTime = Date.now() - startTime;

    res.json({
      status: 'OK',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      responseTime: `${responseTime}ms`,
      database: dbHealth,
      environment: process.env.NODE_ENV || 'development',
    });
  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({
      status: 'ERROR',
      error: 'Health check failed',
    });
  }
};