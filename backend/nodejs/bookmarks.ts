import express from 'express';
import { createBookmark, getBookmarks, deleteBookmark, updateBookmark } from '../controllers/bookmarkController';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

// Protected routes for bookmarks
router.post('/', authenticate, validate('conversation'), createBookmark);
router.get('/', authenticate, getBookmarks);
router.put('/:id', authenticate, updateBookmark);
router.delete('/:id', authenticate, deleteBookmark);

export default router;