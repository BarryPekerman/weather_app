FROM python:3.12-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./weather_app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set working directory back
WORKDIR /app

# Use exec form and specific port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import requests,sys; sys.exit(0 if requests.get('http://localhost:5000/metrics', timeout=5).ok else 1)"

CMD ["python3", "-m", "weather_app.run"]
