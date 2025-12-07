# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src ./src

# Expose port (deployment platform will set PORT env var)
EXPOSE 3000

# Set environment to HTTP transport for deployment
ENV TRANSPORT=http

# Run the server
CMD ["uv", "run", "mcp-ifttt"]
