# Multi-stage build for Django project with uv
ARG VERSION=3.12
FROM python:${VERSION}-slim as base

# Setup environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

# ===== BUILDER STAGE =====
FROM base AS builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy project metadata
WORKDIR /app
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies into a local virtual environment
RUN uv sync --locked --no-dev --no-install-project

# ===== RUNTIME STAGE =====
FROM base AS runtime

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /home/appuser/app/.venv

# Copy project files
COPY --chown=appuser:appuser ./ .

# Switch to non-root user
USER appuser

# Ensure venv binaries are on PATH
ENV PATH="/home/appuser/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --settings=myproject.multiple_db_settings || exit 1
