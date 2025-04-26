import { defineConfig } from "vite";

export default defineConfig({
  server: {
    hmr: {
      overlay: true, // Enable error overlays
    },
  },
});