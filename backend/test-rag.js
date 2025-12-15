// Simple test to check if our RAG function works
const { rag } = require('./dist/rag');

async function testRAG() {
  console.log('Testing RAG function...');
  try {
    const result = await rag('What is Physical AI?');
    console.log('Result:', result);
  } catch (error) {
    console.error('Error in RAG function:', error);
  }
}

testRAG();