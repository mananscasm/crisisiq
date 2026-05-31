import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#101418",
        panel: "rgba(255,255,255,0.08)",
        line: "rgba(255,255,255,0.14)",
        signal: "#2dd4bf",
        risk: "#f97316",
        danger: "#ef4444"
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,.08), 0 20px 60px rgba(0,0,0,.28)"
      }
    }
  },
  plugins: []
};

export default config;
