# Multi-stage Dockerfile for FastAPI app
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip and build wheels for dependencies if requirements exist
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip wheel setuptools
RUN if [ -s /app/requirements.txt ]; then pip wheel --no-cache-dir --wheel-dir /wheels -r /app/requirements.txt; fi

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# runtime deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install wheels (if built)
COPY --from=builder /wheels /wheels
RUN if [ -d /wheels ]; then pip install --no-cache /wheels/*; fi

# Copy project
COPY . /app

# Install runtime requirements (fallback if no wheels)
RUN if [ -s /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

# Ensure entrypoint is executable
RUN chmod +x /app/scripts/docker-entrypoint.sh || true

# Expose port
EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

CMD ["/app/scripts/docker-entrypoint.sh"]
