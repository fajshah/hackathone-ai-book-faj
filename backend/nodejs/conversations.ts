import express from 'express';
import { askQuestion, getConversationHistory, deleteConversation, clearConversationHistory } from '../controllers/conversationController';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

// Public route for asking questions (will save to user's history if authenticated)
router.post('/ask', validate('askQuery'), askQuestion);

// Protected routes for conversation history
router.get('/', authenticate, getConversationHistory);
router.delete('/:id', authenticate, deleteConversation);
router.delete('/', authenticate, clearConversationHistory);

export default router;