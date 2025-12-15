import mongoose from 'mongoose';

// User Schema
const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
  },
  password: {
    type: String,
    required: true,
    minlength: 6,
    select: false, // Don't return password by default
  },
  firstName: {
    type: String,
    required: true,
    maxlength: 50,
  },
  lastName: {
    type: String,
    required: true,
    maxlength: 50,
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user',
  },
  isActive: {
    type: Boolean,
    default: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

// Update the updatedAt field before saving
userSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

// Conversation Schema
const conversationSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  query: {
    type: String,
    required: true,
    maxlength: 1000,
  },
  answer: {
    type: String,
    required: true,
    maxlength: 10000,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
  source: {
    type: String,
    default: 'textbook',
  },
});

// Index for efficient querying by user and timestamp
conversationSchema.index({ userId: 1, timestamp: -1 });

// Bookmark Schema
const bookmarkSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  query: {
    type: String,
    required: true,
    maxlength: 1000,
  },
  answer: {
    type: String,
    required: true,
    maxlength: 10000,
  },
  title: {
    type: String,
    required: true,
    maxlength: 200,
  },
  tags: [{
    type: String,
    maxlength: 50,
  }],
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

// Index for efficient querying by user
bookmarkSchema.index({ userId: 1, createdAt: -1 });

// Create models
export const User = mongoose.model('User', userSchema);
export const Conversation = mongoose.model('Conversation', conversationSchema);
export const Bookmark = mongoose.model('Bookmark', bookmarkSchema);

// Export types
export type UserType = mongoose.Document & {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: 'user' | 'admin';
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
};

export type ConversationType = mongoose.Document & {
  userId: mongoose.Types.ObjectId;
  query: string;
  answer: string;
  timestamp: Date;
  source: string;
};

export type BookmarkType = mongoose.Document & {
  userId: mongoose.Types.ObjectId;
  query: string;
  answer: string;
  title: string;
  tags: string[];
  createdAt: Date;
};