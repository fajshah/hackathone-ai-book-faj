/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Remove the output: 'export' since we have API routes
}

module.exports = nextConfig