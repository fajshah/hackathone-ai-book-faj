import uuid
import time
from typing import Dict, List, Optional, Any
from threading import Lock
from datetime import datetime, timedelta

class SessionManager:
    """
    Simple in-memory session manager for conversation history
    """
    def __init__(self, session_timeout: int = 3600):  # 1 hour default
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = session_timeout
        self._lock = Lock()

    def create_session(self) -> str:
        """Create a new session and return the session ID"""
        session_id = str(uuid.uuid4())
        with self._lock:
            self.sessions[session_id] = {
                'created_at': time.time(),
                'last_accessed': time.time(),
                'conversation_history': []
            }
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a session by ID, returns None if not found or expired"""
        with self._lock:
            if session_id not in self.sessions:
                return None

            session = self.sessions[session_id]

            # Check if session has expired
            if time.time() - session['last_accessed'] > self.session_timeout:
                del self.sessions[session_id]
                return None

            # Update last accessed time
            session['last_accessed'] = time.time()
            return session.copy()

    def add_message_to_session(self, session_id: str, role: str, content: str) -> bool:
        """Add a message to the session's conversation history"""
        with self._lock:
            if session_id not in self.sessions:
                return False

            session = self.sessions[session_id]

            # Check if session has expired
            if time.time() - session['last_accessed'] > self.session_timeout:
                del self.sessions[session_id]
                return False

            # Add message to conversation history
            message = {
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            session['conversation_history'].append(message)
            session['last_accessed'] = time.time()

            # Keep only last 10 messages to prevent memory bloat
            if len(session['conversation_history']) > 10:
                session['conversation_history'] = session['conversation_history'][-10:]

            return True

    def get_conversation_history(self, session_id: str, limit: int = 5) -> List[Dict[str, str]]:
        """Get the conversation history for a session"""
        session = self.get_session(session_id)
        if not session:
            return []

        # Return last 'limit' messages
        return session['conversation_history'][-limit:]

    def clear_expired_sessions(self):
        """Remove expired sessions (called periodically)"""
        with self._lock:
            current_time = time.time()
            expired_sessions = [
                sid for sid, session in self.sessions.items()
                if current_time - session['last_accessed'] > self.session_timeout
            ]

            for sid in expired_sessions:
                del self.sessions[sid]

    def cleanup(self):
        """Clean up all sessions (for shutdown)"""
        with self._lock:
            self.sessions.clear()

# Global session manager instance
session_manager = SessionManager()