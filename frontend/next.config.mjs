import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const isGitHubPages = process.env.GITHUB_PAGES === "true";

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: isGitHubPages ? "export" : "standalone",
  outputFileTracingRoot: __dirname,
  basePath: isGitHubPages ? "/crisisiq" : "",
  assetPrefix: isGitHubPages ? "/crisisiq/" : "",
  trailingSlash: isGitHubPages,
  images: {
    unoptimized: true
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "recharts"]
  }
};

export default nextConfig;
