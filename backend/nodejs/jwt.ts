import jwt from 'jsonwebtoken';
import config from '../config';

// Generate JWT token
export const generateToken = (userId: string): string => {
  // Ensure the secret is treated as a string to avoid type issues
  const secret: string = config.jwtSecret;
  const expiresIn: string = config.jwtExpiresIn;

  // Use type assertion to help TypeScript understand the correct overload
  return jwt.sign({ userId }, secret as jwt.Secret, {
    expiresIn,
  } as jwt.SignOptions);
};

// Verify JWT token
export const verifyToken = (token: string): { userId: string } => {
  const secret: string = config.jwtSecret;
  return jwt.verify(token, secret as jwt.Secret) as { userId: string };
};