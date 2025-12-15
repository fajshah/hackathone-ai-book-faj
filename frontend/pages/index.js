import { useState } from 'react';
import Head from 'next/head';

export default function BookAssistant() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResponse('');

    try {
      const res = await fetch('/api/book-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResponse(data.result);
    } catch (error) {
      setResponse('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>Physical AI & Humanoid Robotics Book Assistant</title>
        <meta name="description" content="Ask questions about Physical AI & Humanoid Robotics" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <header className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-800 mb-4">
              Physical AI & Humanoid Robotics Book Assistant
            </h1>
            <p className="text-lg text-gray-600">
              Ask questions about the textbook and get relevant answers
            </p>
          </header>

          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <form onSubmit={handleSubmit} className="mb-6">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question about Physical AI & Humanoid Robotics..."
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !query.trim()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Searching...' : 'Ask'}
                </button>
              </div>
            </form>

            {response && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-2">Answer:</h3>
                <div className="text-gray-700 whitespace-pre-wrap">{response}</div>
              </div>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">How it works</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Ask questions about Physical AI and Humanoid Robotics</li>
              <li>Our system searches through the textbook content</li>
              <li>Get relevant answers based on the textbook material</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}