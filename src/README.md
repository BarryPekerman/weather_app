# Weather App - Docker Compose Setup

A Flask-based weather application with MongoDB integration that fetches and displays weather forecasts for any given location.

## Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Ports 5000 and 27017 available on your system

### Installation & Running

1. **Clone only the src directory:**
   ```bash
   git clone --filter=blob:none --no-checkout https://github.com/BarryPekerman/weather_app.git
   cd weather_app
   git sparse-checkout init --cone
   git sparse-checkout set src
   git checkout
   cd src
   ```

2. **Start the application:**
   ```bash
   docker compose up -d --build
   ```

3. **Access the application:**
   - Weather App: http://localhost:5000

4. **View logs:**
   ```bash
   docker compose logs -f weather-app
   ```

5. **Stop the application:**
   ```bash
   docker compose down
   ```

## What's Included

This setup includes:
- **Weather App**: Flask application with web UI
- **MongoDB**: Database for storing search history
- **Nginx**: Optional reverse proxy (use `--profile nginx` to enable)

## Services

### Weather App
- **Port**: 5000
- **Health Check**: Available at `/metrics`
- **Features**: Weather search, search history, Prometheus metrics

### MongoDB
- **Port**: 27017
- **Database**: weather
- **User**: weather_user
- **Collections**: search_history
- **Data**: Ephemeral (resets on container restart)

### Nginx (Optional)
- **Port**: 80
- **Usage**: `docker compose --profile nginx up -d`

## Environment Variables

The app uses these environment variables:
- `MONGODB_URI`: MongoDB connection string
- `APP_PORT`: Application port (default: 5000)
- `BG_COLOR`: Background color for UI (default: #0000FF)

## Troubleshooting

1. **Check service status:**
   ```bash
   docker compose ps
   ```

2. **View service logs:**
   ```bash
   docker compose logs [service-name]
   ```

3. **Restart a service:**
   ```bash
   docker compose restart [service-name]
   ```

4. **Clean up everything:**
   ```bash
   docker compose down -v  # Removes volumes too
   ```

