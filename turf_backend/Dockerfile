# Use official lightweight Python 3.12 image
FROM python:3.12-slim

# Prevent Python from writing bytecode and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install PostgreSQL client dependencies & build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY . /app/

# Expose Gunicorn port
EXPOSE 8000

# Collect static files, run database migrations, and start Gunicorn server
CMD ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate && gunicorn turf_backend.wsgi:application --bind 0.0.0.0:8000"]
