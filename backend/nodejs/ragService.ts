import { LocalTextbookService } from './localTextbookService';
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import config from '../config';

export class RAGService {
  private textbookService: LocalTextbookService;
  private llm: ChatGoogleGenerativeAI | null = null;

  constructor() {
    this.textbookService = new LocalTextbookService();

    // Initialize LLM only if API key is available
    if (config.googleApiKey && config.googleApiKey.trim() !== '') {
      try {
        this.llm = new ChatGoogleGenerativeAI({
          apiKey: config.googleApiKey,
          model: "gemini-pro"
        });
      } catch (error) {
        console.warn('Failed to initialize Google LLM:', error);
      }
    }
  }

  async getAnswer(query: string): Promise<string> {
    try {
      // Step 1: Search local textbook content first (primary source)
      const searchResults = await this.textbookService.search(query);
      const relevantSections = searchResults.slice(0, 3); // Get top 3 results

      if (relevantSections.length === 0) {
        return `I couldn't find specific information about "${query}" in the textbook content. The textbook covers topics like Physical AI, Humanoid Robotics, ROS 2, Digital Twin Simulation, AI Robot Brains, Vision-Language-Action Systems, and Autonomous Humanoids. Please try rephrasing your question or check the textbook directly.`;
      }

      // Combine relevant content
      const context = relevantSections.map(match => {
        const title = match.sectionTitle || match.chapterTitle;
        return `## ${title}\n\n${match.content}`;
      }).join('\n\n---\n\n');

      // Step 2: If Google LLM is available, use it to generate a better response
      if (this.llm) {
        try {
          const prompt = `You are an AI assistant specialized in the "Physical AI and Humanoid Robotics" textbook.

          Instructions:
          1. Answer the user's question using the provided textbook content.
          2. Be concise, clear, and informative.
          3. Include references to the chapter or section if available.
          4. If the answer is not in the content, say so clearly.

          User Question: ${query}

          Textbook Content:
          ${context}

          Answer:`;

          const response = await this.llm.invoke(prompt);
          return response.content as string;
        } catch (llmError) {
          console.warn('Google LLM failed, falling back to local processing:', llmError);
          // Continue with local processing below
        }
      }

      // Step 3: Fallback - return the most relevant content directly
      return `Based on the Physical AI and Humanoid Robotics textbook:\n\n${context}\n\nFor more detailed information, please refer to the relevant chapters in the textbook.`;

    } catch (error) {
      console.error('Error in RAGService:', error);
      return `I encountered an error while processing your request: ${error instanceof Error ? error.message : 'Unknown error'}. Please try asking your question again.`;
    }
  }
}

// Export singleton instance
export const ragService = new RAGService();