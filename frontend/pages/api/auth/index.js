// This file serves as a placeholder to maintain the auth API structure
// The actual auth endpoints are implemented in the backend at /api/auth/*
export default function handler(req, res) {
  res.status(404).json({ error: 'Auth endpoints are available in the backend API' });
}