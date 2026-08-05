# Stage 1: Build the React application
FROM node:24-alpine AS builder
WORKDIR /app

# Copy package manifests first to leverage Docker layer caching
COPY /frontend/package*.json ./
RUN npm ci

# Copy the rest of the application files and build the app
COPY /frontend/ ./
RUN npm run build

# Stage 2: Serve the application using Nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the Nginx web server
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]