import React from 'react';
import Layout from '@theme/Layout';
import AskTheBookComponent from "../../../AskTheBook";

export default function AskTheBook() {
  return (
    <Layout
      title="Ask the Book"
      description="Ask questions about the Physical AI & Humanoid Robotics textbook">
      <main>
        <AskTheBookComponent />
      </main>
    </Layout>
  );
}