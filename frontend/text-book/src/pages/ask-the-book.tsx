import React, { useState } from 'react';
import Layout from '@theme/Layout';

export default function AskTheBook() {
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAsk = async () => {
        if (!query) {
            setError('Please enter a question.');
            return;
        }

        setIsLoading(true);
        setError('');
        setAnswer('');

        try {
            const response = await fetch('http://localhost:3001/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error('Failed to get an answer from the server.');
            }

            const data = await response.json();
            setAnswer(data.answer);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout title="Ask the Book" description="Ask questions about the AI Robotics textbook">
            <div className="container" style={{ padding: '2rem' }}>
                <h1>Ask the Book</h1>
                <p>
                    This is an interactive RAG (Retrieval-Augmented Generation) system.
                    Ask a question about the content of the AI Robotics textbook, and the system will try to answer it.
                </p>
                <div style={{ marginBottom: '1rem' }}>
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g., What is Physical AI?"
                        style={{ width: '100%', padding: '0.5rem', fontSize: '1rem' }}
                    />
                </div>
                <div>
                    <button onClick={handleAsk} disabled={isLoading} style={{ padding: '0.5rem 1rem', fontSize: '1rem' }}>
                        {isLoading ? 'Thinking...' : 'Ask'}
                    </button>
                </div>

                {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
                
                {answer && (
                    <div style={{ marginTop: '2rem', whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '1rem', borderRadius: '4px', backgroundColor: '#f9f9f9' }}>
                        <h2>Answer</h2>
                        <p>{answer}</p>
                    </div>
                )}
            </div>
        </Layout>
    );
}
