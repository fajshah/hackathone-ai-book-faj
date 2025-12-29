'use client';

import { useState } from "react";

interface AnswerItem {
  chunk_id?: number;
  content: string;
  score?: number;
  metadata?: Record<string, any>;
}

export default function AskTheBook() {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState<AnswerItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  // Determine backend URL based on environment
  const isDevelopment = typeof window !== 'undefined' && window.location.hostname === 'localhost';
  const API_URL = isDevelopment
    ? "http://localhost:8002/api/ask/public"
    : "https://fajji-backend-chatbot.hf.space/api/ask/public";
  const IFRAME_URL = isDevelopment
    ? "http://localhost:8002"
    : "https://fajji-backend-chatbot.hf.space";

  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(false);
    setAnswers([]);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, top_k: 5 })
      });

      if (!res.ok) throw new Error(`API Error: ${res.status}`);
      const data = await res.json();

      // Display the main answer, not the sources
      setAnswers([{
        content: data.answer || "No answer available",
      }]);
    } catch (err) {
      console.error("API fetch error:", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: "900px",
      margin: "20px auto",
      padding: "16px",
      border: "1px solid #ddd",
      borderRadius: "12px",
      backgroundColor: "#fff",
      boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
    }}>
      <h2 style={{ marginBottom: "12px", color: "#7c3aed" }}>Ask the Book</h2>

      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "12px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          fontSize: "16px",
          boxSizing: "border-box"
        }}
      />

      <button
        onClick={askQuestion}
        disabled={loading || !question.trim()}
        style={{
          width: "100%",
          padding: "10px",
          backgroundColor: "#7c3aed",
          color: "#fff",
          fontSize: "16px",
          fontWeight: 500,
          border: "none",
          borderRadius: "6px",
          cursor: loading || !question.trim() ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Loading..." : "Ask"}
      </button>

      {error && (
        <div style={{ marginTop: "20px" }}>
          <p style={{ color: "red", marginBottom: "12px" }}>
            API failed. Loading fallback...
          </p>
          <iframe
            src={IFRAME_URL}
            width="100%"
            height="450"
            style={{ border: "1px solid #ccc", borderRadius: "12px" }}
            title="Ask the Book Fallback"
            allowFullScreen
          ></iframe>
        </div>
      )}

      {answers.length > 0 && !error && (
        <div style={{ marginTop: "20px" }}>
          {answers.map((ans, idx) => (
            <div key={idx} style={{
              padding: "10px",
              border: "1px solid #e5e7eb",
              borderRadius: "6px",
              backgroundColor: "#f9fafb",
              wordBreak: "break-word"
            }}>
              <p style={{ margin: "0", lineHeight: "1.6" }}>{ans.content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}