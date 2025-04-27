import { defineConfig } from "vite";
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    hmr: {
      overlay: true, // Enable error overlays
    },
  },
});
