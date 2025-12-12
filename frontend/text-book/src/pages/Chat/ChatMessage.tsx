import React from 'react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: Date;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isUser, timestamp }) => {
  const messageClass = isUser
    ? 'chat-message-user'
    : 'chat-message-assistant';

  const messageRole = isUser ? 'You' : 'Book Assistant';

  return (
    <div className={`chat-message ${messageClass}`}>
      <div className="chat-message-header">
        <strong>{messageRole}</strong>
        {timestamp && (
          <span className="chat-timestamp">
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        )}
      </div>
      <div className="chat-message-content">
        {message}
      </div>
    </div>
  );
};

export default ChatMessage;  