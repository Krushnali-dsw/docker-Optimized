# Multi-stage build for ultra-small image
FROM python:3.11-slim as builder

# Install minimal build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install dependencies to a specific directory
RUN pip install --target=/app/deps --no-cache-dir -r requirements.txt

# Final stage: Distroless Python
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy Python dependencies
COPY --from=builder /app/deps /app/deps

# Copy application code
COPY main.py .

# Set Python path to include dependencies
ENV PYTHONPATH=/app/deps

EXPOSE 8000

# Use the python3 executable from distroless
ENTRYPOINT ["python3"]
CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]