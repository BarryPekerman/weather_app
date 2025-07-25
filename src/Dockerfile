
FROM python:3.12-slim

WORKDIR /weather_app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

WORKDIR /

CMD ["python3","-m","weather_app.run"]

