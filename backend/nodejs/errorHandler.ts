import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';

// Custom error class
export class AppError extends Error {
  public statusCode: number;
  public isOperational: boolean;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

// Global error handler middleware
export const globalErrorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  let { statusCode, message } = err as AppError;

  // Log the error
  logger.error(`${req.method} ${req.originalUrl} - ${err.message} - ${err.stack}`);

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    message = 'Resource not found';
    statusCode = 404;
  }

  // Mongoose duplicate key
  if ('code' in err && (err as any).code === 11000) {
    message = 'Duplicate field value entered';
    statusCode = 400;
  }

  // Mongoose validation error
  if (err.name === 'ValidationError' && 'errors' in err) {
    const error = err as any;
    message = Object.values(error.errors)
      .map((value: any) => value.message)
      .join(', ');
    statusCode = 400;
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    message = 'Invalid token';
    statusCode = 401;
  }

  if (err.name === 'TokenExpiredError') {
    message = 'Token expired';
    statusCode = 401;
  }

  res.status(statusCode || 500).json({
    success: false,
    error: message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};

// 404 handler
export const notFoundHandler = (req: Request, res: Response, next: NextFunction): void => {
  const error = new AppError(`Route not found: ${req.originalUrl}`, 404);
  next(error);
};