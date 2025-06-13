# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including git
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

RUN middleware-bootstrap -a install

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GIT_PYTHON_REFRESH=quiet

# Expose the port the app runs on
EXPOSE 8000

ENV MW_API_KEY=lneevcqdcnzccpdpbhelkxpjffdxeznkryvb
ENV MW_TARGET=https://ruplp.middleware.io:443
ENV MW_SERVICE_NAME=uvicorn-trhealth-test
ENV OTEL_PROPAGATORS=traceparent

# Use middleware-run as the entrypoint
ENTRYPOINT ["middleware-run"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]