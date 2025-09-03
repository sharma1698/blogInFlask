FROM python:3.11 AS base

FROM base AS builder

WORKDIR /app

# Install core dependencies.
# The --no-install-recommends flag keeps the image size smaller.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libssl-dev \
    ca-certificates \
    default-libmysqlclient-dev \
    gcc \
    libmariadb3 \
    #used when mysql is using
    && rm -rf /var/lib/apt/lists/*

# Install the necessary Python package directly.below line only for production
# RUN pip install gunicorn --no-cache-dir

# Copy the requirements file
COPY requirements.txt .
# This assumes you have already copied a `requirements.txt` file into the container.
# The --no-cache-dir flag reduces the image size.
RUN pip install --no-cache-dir --default-timeout 100 -r requirements.txt



# Stage 2: The Final Production Image
FROM base AS runner

WORKDIR /home/app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code
COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH

# Expose the port Flask runs on (default is 5000)
EXPOSE 5000
# This tells Flask where to find your application
ENV FLASK_APP=main.py

# Set Flask to production mode
ENV FLASK_ENV=production

# Use a production WSGI server (Gunicorn) to run the application
# This is much more robust than the built-in Flask server.
# Assumes 'app' is the name of your Flask instance in main.py
# gunicorn for production
# CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

# for local
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]



