FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* npm-shrinkwrap.json* ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy app
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Run app
CMD ["npm", "start"]
