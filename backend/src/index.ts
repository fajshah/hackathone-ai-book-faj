import express from 'express';
import cors from 'cors';
import { rag } from './rag';

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.post('/api/ask', async (req, res) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const answer = await rag(query);
    res.json({ answer });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to get an answer' });
  }
});

app.listen(port, () => {
  console.log(`Backend server listening at http://localhost:${port}`);
});
