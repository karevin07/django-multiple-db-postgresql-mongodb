# Multi-stage build for Django project with Poetry
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

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry
RUN poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml ./

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi --no-root

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

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY --chown=appuser:appuser ./ .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --settings=myproject.multiple_db_settings || exit 1

# # Default command
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=myproject.multiple_db_settings"]
