#!/bin/bash

echo "Waiting for the database..."

# Use Python to wait for the DB instead of netcat
python << END
import socket, time

host = "db"
port = 3306

while True:
    try:
        socket.create_connection((host, port), timeout=2)
        print("Database is available!")
        break
    except OSError:
        print("Database is unavailable - sleeping")
        time.sleep(1)
END

echo "Database is up! Applying migrations..."
flask db upgrade

echo "Starting Flask application..."
exec flask run --host=0.0.0.0
