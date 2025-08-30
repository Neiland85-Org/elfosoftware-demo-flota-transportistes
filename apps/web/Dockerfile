# Dockerfile for Frontend (Next.js)
FROM node:24-alpine

# Create non-root user
RUN addgroup -g 1001 nodejs && \
    adduser -u 1001 -S nextjs -G nodejs

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Set ownership and switch to non-root user
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
