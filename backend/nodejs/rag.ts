import { RAGService } from './services/ragService';

// Create a singleton instance of the RAG service
const ragService = new RAGService();

// Wrapper function to maintain compatibility with existing code
export async function rag(query: string): Promise<string> {
  return await ragService.getAnswer(query);
}

// Export the service for direct use if needed
export { ragService };