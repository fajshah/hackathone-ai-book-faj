import React, { useState } from 'react';
import Layout from '@theme/Layout';
import ChatWindow from '../../pages/Chat/ChatWindow';
import ChatInput from '../../pages/Chat/ChatInput';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export default function AskTheBook() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSendMessage = async (message: string) => {
    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      text: message,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError('');

    try {
      // Use a configurable backend URL based on environment
      // For local development vs deployed environment
      // IMPORTANT: Update this URL when you deploy your backend to a public server
      const BACKEND_URL = (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1')
                         ? '/api' // Use relative path for Vercel deployment (if backend is deployed with Vercel)
                         : 'http://localhost:8000';

      // For local development, use full API path; for deployed, use relative path
      // Use the public endpoint that doesn't require authentication
      const apiPath = BACKEND_URL.startsWith('http://localhost') ? '/api/ask/public' : '/ask/public';
      const response = await fetch(`${BACKEND_URL}${apiPath}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Server error');
      }

      // Add assistant response to the chat
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to reach backend server.');

      // Add error message to the chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Error: ${err.message || 'Failed to reach backend server.'}`,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout title="Ask the Book" description="Ask questions about the AI Robotics textbook">
      <div className="container" style={{ padding: '2rem' }}>
        <h1>Ask the Book</h1>
        <p>
          This is an interactive RAG system. Ask a question about the textbook.
        </p>

        <div className="chat-container">
          <ChatWindow messages={messages} isLoading={isLoading} />
          <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>

        {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
      </div>
    </Layout>
  );
}
