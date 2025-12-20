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
      // Get token from localStorage (assuming it's stored after login)
      const token = localStorage.getItem('access_token');

      const response = await fetch('http://localhost:8000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
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
