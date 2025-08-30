/** @type {import("next").NextConfig} */
const nextConfig = {
  experimental: {
    // appDir: true,  // ← Removida - opción obsoleta
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
};

module.exports = nextConfig;
