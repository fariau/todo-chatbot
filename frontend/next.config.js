/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  },
  output: 'export', // Enable static exports for GitHub Pages
  trailingSlash: true, // Add trailing slashes to make routing work properly
  images: {
    unoptimized: true, // Disable image optimization for static exports
  },
}

module.exports = nextConfig