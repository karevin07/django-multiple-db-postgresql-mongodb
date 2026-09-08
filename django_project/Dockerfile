# Multi-stage build for Django project with uv
# Build context is ./django_project (see `make build-django-image`).
ARG VERSION=3.12
FROM python:${VERSION}-slim AS base

# Setup environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # Keep the virtualenv outside the app directory so a bind-mounted source
    # tree (docker-compose) does not shadow the installed dependencies.
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH

# ===== BUILDER STAGE =====
FROM base AS builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv from its official (pinned) image
COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /bin/uv

WORKDIR /home/appuser/app

# Copy project metadata (build context is ./django_project)
COPY pyproject.toml uv.lock ./

# Install dependencies into /opt/venv
RUN uv sync --locked --no-dev --no-install-project

# ===== RUNTIME STAGE =====
FROM base AS runtime

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy the virtual environment from the builder stage (same path -> valid shebangs)
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Set working directory and copy project files (build context is ./django_project)
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check: confirm the app is actually serving HTTP (not just importable)
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/admin/login/', timeout=5).status < 500 else 1)"
