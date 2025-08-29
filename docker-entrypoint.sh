#!/bin/sh

# This script ensures the database is ready, runs migrations, and starts the Flask app.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Wait for MySQL to be ready ---
# This loop checks if the MySQL server is accepting connections.
# It uses the 'db' hostname and default MySQL port 3306.
# Adjust timeout and sleep as necessary for your environment.
echo "Waiting for MySQL database to be ready..."
until mysqladmin ping -h "db"    --silent; do
  echo "MySQL is unavailable - sleeping"
  sleep 5 # Wait for 5 seconds before retrying
done
echo "MySQL is up and running!"

# --- Run Flask Migrations ---
# Ensure Flask-Migrate commands are run within the Flask application context.
# 'flask db upgrade' applies all pending migrations.
echo "Running Flask database migrations..."
flask db upgrade
echo "Flask database migrations applied."

# --- Start the Flask application with Gunicorn ---
# This should be the last command in the script, as it keeps the container running.
echo "Starting Flask application with Gunicorn..."
# Use the full path for gunicorn to ensure the command is always found.
exec /usr/local/bin/gunicorn --bind 0.0.0.0:5000 main:app
