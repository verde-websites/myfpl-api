# Use the official MySQL image from Docker Hub
FROM mysql:8.0

# Set environment variables for MySQL
ENV MYSQL_DATABASE=fplhub \
    MYSQL_ROOT_PASSWORD=passwordisgod \
    MYSQL_USER=fplhub \
    MYSQL_PASSWORD=passwordisgod

# Copy any custom initialization SQL scripts (if needed)
# ADD ./init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306
