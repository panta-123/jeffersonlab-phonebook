// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react"; // Import the React plugin
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(), // Add the React plugin here
    tailwindcss(),
  ],
  server: {
    proxy: {
      '/api/v1': {
        target: 'http://backend:8000', // Your actual backend URL
        changeOrigin: false, // Needed for virtual hosted sites
        secure: false,       // JLab uses a valid SSL certificate, so keep this true
      },
    },
  },
});