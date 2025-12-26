import React, { useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const AskTheBookComponent: React.FC = () => {
  const [query, setQuery] = useState('');
  const [conversation, setConversation] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);

    // Add user's question to conversation
    const userMessage: Message = {
      role: 'user',
      content: query,
      timestamp: new Date()
    };

    setConversation(prev => [...prev, userMessage]);

    try {
      // Prepare context from previous conversation (last 3 exchanges)
      const context = conversation.slice(-3).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Check if we're in development mode (localhost) or production
      const isDevelopment = typeof window !== 'undefined' && window.location.hostname === 'localhost';
      const BACKEND_URL = isDevelopment
        ? 'http://localhost:8000'
        : 'https://fajji-backend-chatbot.hf.space';
      const res = await fetch(`${BACKEND_URL}/api/ask/public`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: query,
          top_k: 5,
          conversation_context: context,
          session_id: sessionId
        }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `API request failed with status ${res.status}`);
      }

      const data = await res.json();

      // Update session ID if returned from backend
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      // Add assistant's response to conversation
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer || 'No response received',
        timestamp: new Date()
      };

      setConversation(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);

      // Add error message to conversation
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Error: ' + (error as Error).message,
        timestamp: new Date()
      };

      setConversation(prev => [...prev, errorMessage]);
    } finally {
      setQuery(''); // Clear the input after submission
      setLoading(false);
    }
  };

  return (
    <div className="container margin-vert--xl">
      <div className="row">
        <div className="col col--8 col--offset-2">
          <h1 className="text--center margin-bottom--lg">Ask the Book</h1>

          <form onSubmit={handleSubmit} className="margin-bottom--lg">
            <div className="form-group">
              <div className="input-group input-group--outline">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question about Physical AI & Humanoid Robotics..."
                  className="form-control"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !query.trim()}
                  className="button button--primary"
                >
                  {loading ? 'Searching...' : 'Ask'}
                </button>
              </div>
            </div>
          </form>

          {conversation.length > 0 && (
            <div className="chat-history">
              {conversation.map((message, index) => (
                <div
                  key={index}
                  className={`margin-bottom--md ${message.role === 'user' ? 'text--left' : 'text--left'}`}
                >
                  <div className={`alert ${message.role === 'user' ? 'alert--secondary' : 'alert--info'}`}>
                    <small className="text--uppercased text--bold">
                      {message.role === 'user' ? 'You:' : 'Assistant:'}
                    </small>
                    <div className="markdown">
                      {message.content.split('\n').map((line, i) => (
                        <p key={i}>{line}</p>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="card margin-top--lg">
            <div className="card__header">
              <h3>How it works</h3>
            </div>
            <div className="card__body">
              <ul>
                <li>Ask questions about Physical AI and Humanoid Robotics</li>
                <li>Our system searches through the textbook content</li>
                <li>Get relevant answers based on the textbook material</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AskTheBookComponent;