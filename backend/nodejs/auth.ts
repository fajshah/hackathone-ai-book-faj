import express from 'express';
import { register, login, getProfile, updateProfile } from '../controllers/authController';
import { validate } from '../middleware/validation';

const router = express.Router();

// Public routes
router.post('/register', validate('userRegister'), register);
router.post('/login', validate('userLogin'), login);

// Protected routes
router.get('/profile', getProfile);
router.put('/profile', updateProfile);

export default router;