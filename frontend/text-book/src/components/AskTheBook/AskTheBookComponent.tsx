import React from 'react';

const AskTheBookComponent: React.FC = () => {
  return (
    <div className="container margin-vert--xl">
      <div className="row">
        <div className="col col--10 col--offset-1">
          <h1 className="text--center margin-bottom--lg">Ask the Book</h1>

          <div style={{ maxWidth: '900px', margin: '20px auto' }}>
            <iframe
              src="https://fajji-backend-chatbot.hf.space"
              width="100%"
              height="500"
              style={{ border: '2px solid #e0e0e0', borderRadius: '12px' }}
              title="Ask the Book"
              allowFullScreen
            ></iframe>
          </div>

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