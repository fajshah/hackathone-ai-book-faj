# Physical AI & Humanoid Robotics Book Assistant

A Next.js application that allows users to ask questions about the Physical AI & Humanoid Robotics textbook and get relevant answers based on the content stored in Qdrant vector database.

## Architecture Note

This repository contains multiple separate applications:
1. **Documentation Site**: Docusaurus site in `frontend/text-book/` directory (http://localhost:3000) - **CONTENT ONLY**
2. **Backend Service**: Authentication and API in `backend/` directory (http://localhost:8001)
3. **Frontend App**: Next.js RAG interface in `frontend/` directory

**CRITICAL**: The documentation site (Docusaurus) is strictly for content delivery and must remain separated from authentication functionality.

## Features

- Interactive chat interface for asking questions
- Semantic search through textbook content using Qdrant
- Integration with OpenAI embeddings for query processing
- Responsive design with Tailwind CSS

## Prerequisites

- Node.js 18+ installed
- OpenAI API key (optional, mock embeddings work without it)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Note: The application will work with mock embeddings if you don't provide an OpenAI API key.

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Documentation Site Setup

To run the Docusaurus documentation site:
```bash
cd frontend/text-book
npm run start
```

The documentation site will be available at http://localhost:3000

## Deployment to Vercel

### Option 1: One-Click Deploy
[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/physical-ai-book-assistant&env=OPENAI_API_KEY)

### Option 2: Manual Deployment

1. Install the Vercel CLI:
```bash
npm i -g vercel
```

2. Link your project to Vercel:
```bash
vercel
```

3. Set your environment variables in the Vercel dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)

4. Deploy:
```bash
vercel --prod
```

### Option 3: Git Integration

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Go to [vercel.com](https://vercel.com) and create a new project
3. Import your repository
4. Add the environment variable `OPENAI_API_KEY` in the Environment Variables section
5. Click "Deploy" and your application will be live!

## Project Structure

```
frontend/
├── text-book/            # Docusaurus documentation site (CONTENT ONLY)
├── pages/
│   ├── index.js          # Main application page
│   └── api/
│       └── book-assistant.js  # API route for Qdrant search
├── package.json          # Dependencies and scripts
└── README.md             # This file
```

## How It Works

1. User enters a question in the input field
2. Frontend sends the query to the `/api/book-assistant` endpoint
3. The API route:
   - Generates an embedding for the query (using OpenAI or mock)
   - Searches for similar content in the Qdrant `physical_ai` collection
   - Returns the top 5 matching sections
4. Frontend displays the concatenated results

## Technologies Used

- Next.js for the React framework
- Tailwind CSS for styling
- Qdrant for vector similarity search
- OpenAI for text embeddings
- Vercel for deployment
- Docusaurus for documentation (in text-book/)

## Architecture Constraints

- **Documentation Site**: The Docusaurus site in `frontend/text-book/` is for content only
- **No Auth Integration**: Authentication functionality is completely separated
- **Preserve Classic UI**: Docusaurus maintains default theme styling
- **Content Focus**: Documentation site should never contain auth components

## Notes

- The application is already connected to the Qdrant Cloud instance containing the textbook content
- Without an OpenAI API key, the system uses deterministic mock embeddings which still provide reasonable search results
- The Qdrant collection name is `physical_ai` and contains all textbook chapters and sections