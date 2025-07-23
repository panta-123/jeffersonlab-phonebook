// Simple version that works directly in browsers
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api/v1'
    : 'https://api.yourdomain.com';