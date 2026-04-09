# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies needed for building
RUN apt-get update && \
    apt-get --yes --no-install-recommends install \
    build-essential \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment to install dependencies in the build stage
RUN python -m venv /opt/venv

# Activate virtual environment and install Python dependencies
ENV PATH="/opt/venv/bin:$PATH"
COPY maktabiya-app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime stage
FROM python:3.12-slim

# Set environment variables
ENV APP_VERSION=1.2.3 \
    BETTER_EXCEPTIONS=1 \
    DJANGO_SUPERUSER_EMAIL=admin@AladinStudioX.app \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_USERNAME=admin \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1  \
    PATH="/opt/venv/bin:$PATH"

# ARG for UID and GID
ARG UID=1000 GID=1000

# Install runtime dependencies (only what’s necessary for running the app)
RUN apt-get update && \
    apt-get --yes --no-install-recommends install \
    curl \
    wait-for-it \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv


# Create app directory and copy code
RUN mkdir /app
WORKDIR /app
COPY maktabiya-app/ /app/

# Create non-root user and set ownership
RUN groupadd -g "${GID}" -r maktabiya \
  && useradd -d '/app' -g maktabiya -l -r -u "${UID}" maktabiya \
  && chown maktabiya:maktabiya -R '/app' \
  && chmod +x /app/entrypoint.sh

# Run as non-root user
USER maktabiya

# Expose the port and set the entry point
EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
