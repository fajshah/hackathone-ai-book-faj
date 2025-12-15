import { QdrantClient } from '@qdrant/js-client-rest';
import { OpenAI } from 'openai';

// Initialize Qdrant client
const qdrantClient = new QdrantClient({
  url: 'https://bef512c4-0759-464d-af6c-4d6e2352566c.us-east4-0.gcp.cloud.qdrant.io',
  apiKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jCpXlK2HGZIHrE5j4iXF1cfFAthAmzXH-Kw-SSUhNFI',
});

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    // Generate embedding for the query
    let embedding;
    if (process.env.OPENAI_API_KEY) {
      const response = await openai.embeddings.create({
        input: query,
        model: 'text-embedding-ada-002',
      });
      embedding = response.data[0].embedding;
    } else {
      // Generate a deterministic mock embedding if no API key is provided
      const textHash = hashString(query);
      embedding = generateMockEmbedding(textHash, 1536);
    }

    // Search for similar sections in Qdrant
    const searchResponse = await qdrantClient.search('physical_ai', {
      vector: embedding,
      limit: 5,
      with_payload: true,
    });

    // Concatenate the text from the top 5 results
    const results = searchResponse.map((hit) => {
      const payload = hit.payload;
      return `Chapter: ${payload.chapter}\nSection: ${payload.section}\nContent: ${payload.text}`;
    });

    const resultText = results.join('\n\n---\n\n');

    res.status(200).json({ result: resultText });
  } catch (error) {
    console.error('Error in book assistant API:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

// Helper function to generate a deterministic mock embedding
function generateMockEmbedding(seed, size) {
  const embedding = new Array(size);
  for (let i = 0; i < size; i++) {
    const value = Math.sin(seed + i) * Math.cos(seed * i);
    embedding[i] = value;
  }
  return embedding;
}

// Helper function to create a hash from a string
function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash);
}