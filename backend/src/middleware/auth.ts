import { Request, Response, NextFunction } from 'express';
import { generateToken, verifyToken } from '../utils/jwt';
import { User, UserType } from '../models';

// Extend Express Request type to include user
declare global {
  namespace Express {
    interface Request {
      user?: UserType;
    }
  }
}

// Authentication middleware
export const authenticate = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : null;

    if (!token) {
      res.status(401).json({ error: 'Access token is required' });
      return;
    }

    // Verify token
    const decoded = verifyToken(token);

    // Get user from database
    const user = await User.findById(decoded.userId).select('-password');

    if (!user) {
      res.status(401).json({ error: 'User not found' });
      return;
    }

    // Attach user to request
    req.user = user;
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(403).json({ error: 'Invalid or expired token' });
  }
};

// Authorization middleware for admin roles
export const authorizeAdmin = (req: Request, res: Response, next: NextFunction): void => {
  if (!req.user) {
    res.status(401).json({ error: 'Authentication required' });
    return;
  }

  if (req.user.role !== 'admin') {
    res.status(403).json({ error: 'Admin access required' });
    return;
  }

  next();
};