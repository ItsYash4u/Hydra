# Using a slim Python image for a smaller footprint
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project files
COPY . .

# Collect static files
# Note: In production, Whitenoise or S3 will handle these.
# Environment variables like DJANGO_SECRET_KEY might be needed here if not using a dummy during build.
RUN python manage.py collectstatic --noinput --settings=config.settings.production || true

# Expose port
EXPOSE 8000

# Run gunicorn
# Note: Using gunicorn for WSGI. If WebSockets are enabled later, use daphne.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
