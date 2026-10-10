# Production Dockerfile for Counterfeit Detector
# Deploys Unified FastAPI Backend & Web SPA Platform
FROM python:3.11-slim-bookworm AS runtime

# System runtime dependencies & optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/services/api:/app/packages" \
    PORT=8000

WORKDIR /app

# Install minimal OS dependencies for healthchecks and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Layer 1: Python dependencies (cached if requirements don't change)
COPY services/api/requirements.txt /app/services/api/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/services/api/requirements.txt

# Layer 2: Copy application components
COPY apps /app/apps
COPY packages /app/packages
COPY services /app/services

# Security: Non-root user execution
RUN useradd -u 1000 -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose target port (Railway will map this via $PORT)
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/v1/health || exit 1

# Production startup command using dynamic $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2 --access-log"]
