import { Request, Response } from 'express';
import { Conversation, ConversationType } from '../models';
import { RAGService } from '../services/ragService';

// Initialize the RAG service
const ragService = new RAGService();

// Ask question and save conversation
export const askQuestion = async (req: Request, res: Response): Promise<void> => {
  try {
    const { query } = req.body;
    const userId = req.user?._id;

    // Get answer from RAG system
    const answer = await ragService.getAnswer(query);

    // Create conversation record if user is authenticated
    if (userId) {
      const conversation = new Conversation({
        userId,
        query,
        answer,
        source: 'textbook',
      });

      await conversation.save();
    }

    res.json({
      answer,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Ask question error:', error);
    res.status(500).json({ error: 'Failed to get an answer' });
  }
};

// Get user's conversation history
export const getConversationHistory = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { limit = 20, page = 1 } = req.query;

    const limitNum = parseInt(limit as string, 10) || 20;
    const pageNum = parseInt(page as string, 10) || 1;

    // Calculate skip value for pagination
    const skip = (pageNum - 1) * limitNum;

    const conversations = await Conversation
      .find({ userId: req.user._id })
      .sort({ timestamp: -1 }) // Sort by newest first
      .skip(skip)
      .limit(limitNum);

    // Get total count for pagination info
    const total = await Conversation.countDocuments({ userId: req.user._id });

    res.json({
      conversations,
      pagination: {
        currentPage: pageNum,
        totalPages: Math.ceil(total / limitNum),
        totalItems: total,
        itemsPerPage: limitNum,
      },
    });
  } catch (error) {
    console.error('Get conversation history error:', error);
    res.status(500).json({ error: 'Failed to get conversation history' });
  }
};

// Delete a specific conversation
export const deleteConversation = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { id } = req.params;

    const conversation = await Conversation.findOneAndDelete({
      _id: id,
      userId: req.user._id,
    });

    if (!conversation) {
      res.status(404).json({ error: 'Conversation not found' });
      return;
    }

    res.json({ message: 'Conversation deleted successfully' });
  } catch (error) {
    console.error('Delete conversation error:', error);
    res.status(500).json({ error: 'Failed to delete conversation' });
  }
};

// Clear all conversations for user
export const clearConversationHistory = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    await Conversation.deleteMany({ userId: req.user._id });

    res.json({ message: 'Conversation history cleared successfully' });
  } catch (error) {
    console.error('Clear conversation history error:', error);
    res.status(500).json({ error: 'Failed to clear conversation history' });
  }
};