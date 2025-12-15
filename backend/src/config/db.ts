import mongoose from 'mongoose';
import config from './index';

export const connectDB = async (): Promise<void> => {
  try {
    const conn = await mongoose.connect(config.mongoUri);

    console.log(`MongoDB Connected: ${conn.connection.host}`);

    // Log connection events
    mongoose.connection.on('error', (err) => {
      console.error('MongoDB connection error:', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.log('MongoDB disconnected');
    });

    // Graceful shutdown
    process.on('SIGINT', async () => {
      await mongoose.connection.close();
      console.log('MongoDB connection closed through app termination');
      process.exit(0);
    });
  } catch (error) {
    console.warn('Warning: Could not connect to MongoDB. Running in limited mode:', error);
    // Don't exit the process, continue without database
    // This allows the server to run for API endpoints that don't require database
  }
};