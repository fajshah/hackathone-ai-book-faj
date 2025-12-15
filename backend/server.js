const express = require('express');
const cors = require('cors');
const { askQuestion } = require('./api/ask');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// API endpoint to ask questions
app.post('/api/ask', async (req, res) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const answer = await askQuestion(query);
    res.json({ answer });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to get an answer' });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({ message: 'AI Textbook Backend API', version: '1.0.0' });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

module.exports = app;