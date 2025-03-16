# pulling base image
FROM nginx:latest

# remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY django.conf /etc/nginx/conf.d/django.conf

# Create directory for static files
RUN mkdir -p /var/www/html/static

# Expose port 80
EXPOSE 80