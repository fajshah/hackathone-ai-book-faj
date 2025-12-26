#!/usr/bin/env node

// start_better_auth.js
const { spawn } = require('child_process');

console.log('Starting Better Auth Service...');

// Set the environment
const env = { ...process.env, NODE_ENV: 'development' };

// Start the TypeScript node server using the local ts-node
const server = spawn('node_modules/.bin/ts-node', ['src/index.ts'], {
  stdio: 'inherit',
  env: env,
  cwd: __dirname
});

server.on('error', (err) => {
  console.error('Failed to start Better Auth Service:', err);
  console.error('Make sure you have installed all dependencies with: npm install');
  process.exit(1);
});

server.on('close', (code) => {
  console.log(`Better Auth Service exited with code ${code}`);
  process.exit(code);
});

console.log('Better Auth Service started on port 8002');
console.log('API endpoints available at: http://localhost:8002/api/auth/better');