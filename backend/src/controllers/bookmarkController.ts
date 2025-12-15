import { Request, Response } from 'express';
import { Bookmark, BookmarkType } from '../models';

// Create a new bookmark
export const createBookmark = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { query, answer, title, tags } = req.body;

    const bookmark = new Bookmark({
      userId: req.user._id,
      query,
      answer,
      title,
      tags: tags || [],
    });

    await bookmark.save();

    res.status(201).json({
      message: 'Bookmark created successfully',
      bookmark,
    });
  } catch (error) {
    console.error('Create bookmark error:', error);
    res.status(500).json({ error: 'Failed to create bookmark' });
  }
};

// Get user's bookmarks
export const getBookmarks = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { limit = 20, page = 1, tag } = req.query;

    const limitNum = parseInt(limit as string, 10) || 20;
    const pageNum = parseInt(page as string, 10) || 1;

    // Build query
    const query: any = { userId: req.user._id };
    if (tag) {
      query.tags = { $in: [tag] };
    }

    // Calculate skip value for pagination
    const skip = (pageNum - 1) * limitNum;

    const bookmarks = await Bookmark
      .find(query)
      .sort({ createdAt: -1 }) // Sort by newest first
      .skip(skip)
      .limit(limitNum);

    // Get total count for pagination info
    const total = await Bookmark.countDocuments(query);

    res.json({
      bookmarks,
      pagination: {
        currentPage: pageNum,
        totalPages: Math.ceil(total / limitNum),
        totalItems: total,
        itemsPerPage: limitNum,
      },
    });
  } catch (error) {
    console.error('Get bookmarks error:', error);
    res.status(500).json({ error: 'Failed to get bookmarks' });
  }
};

// Delete a bookmark
export const deleteBookmark = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { id } = req.params;

    const bookmark = await Bookmark.findOneAndDelete({
      _id: id,
      userId: req.user._id,
    });

    if (!bookmark) {
      res.status(404).json({ error: 'Bookmark not found' });
      return;
    }

    res.json({ message: 'Bookmark deleted successfully' });
  } catch (error) {
    console.error('Delete bookmark error:', error);
    res.status(500).json({ error: 'Failed to delete bookmark' });
  }
};

// Update a bookmark
export const updateBookmark = async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'User not authenticated' });
      return;
    }

    const { id } = req.params;
    const { title, tags } = req.body;

    const bookmark = await Bookmark.findOneAndUpdate(
      { _id: id, userId: req.user._id },
      { title, tags },
      { new: true, runValidators: true }
    );

    if (!bookmark) {
      res.status(404).json({ error: 'Bookmark not found' });
      return;
    }

    res.json({
      message: 'Bookmark updated successfully',
      bookmark,
    });
  } catch (error) {
    console.error('Update bookmark error:', error);
    res.status(500).json({ error: 'Failed to update bookmark' });
  }
};