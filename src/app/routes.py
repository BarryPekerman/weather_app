from flask import Blueprint, request, render_template, Response
from ..services.weather_app_service import WeatherAppService
from ..app.database import MongoDBService
import logging
from prometheus_client import Counter, start_http_server, generate_latest, REGISTRY
from datetime import datetime, timezone
import os

# Import loggers
from ..app.loggers import event_logger

# Configure routes
home_bp = Blueprint('home', __name__)
history_bp = Blueprint('history', __name__)

# Initialize MongoDB service
db_service = MongoDBService()

# Configure prometheus counter
city_requests = Counter(
    'city_requests_total',
    'Total number of HTTP requests for city searches',
    ['city']
)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    weather_forecast = None
    error = None
    bg_color = os.getenv("BG_COLOR", "#0000FF")
    
    try:
        int(bg_color.lstrip("#"), 16)
    except ValueError:
        event_logger.exception(f"Invalid BG_COLOR value: '{bg_color}' is not a valid hexadecimal color.")
        raise
    
    if request.method == "POST":
        location_name = request.form.get("locname", "").strip()
        days = request.form.get("days")
        weather_forecast, location_data = WeatherAppService.get_weather_forecast(location_name, days)
        
        if not weather_forecast:
            event_logger.error(f"Failed to fetch weather data for location: {location_name}")
            error = f"Failed to fetch weather data for location: {location_name}"
        elif weather_forecast.is_empty():
            event_logger.warning(f"No weather data found for location: {location_name}")
            error = f"No weather data found for location: {location_name}"
        else:
            # Save to MongoDB instead of logging to file
            db_service.save_search(location_data.get_name(), weather_forecast)
        
        city_requests.labels(city=location_name).inc()
    
    return render_template("home.html", weather=weather_forecast, bg_color=bg_color, error=error)

@home_bp.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(REGISTRY), mimetype="text/plain")

@history_bp.route('/history')
def view_history():
    # Get date filter from query parameters
    date_str = request.args.get('date')
    selected_date = None
    
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            history_data = db_service.get_search_history_by_date(selected_date)
        except ValueError:
            history_data = db_service.get_search_history()
    else:
        history_data = db_service.get_search_history()
    
    # Format the data for the template
    formatted_history = []
    for entry in history_data:
        formatted_history.append({
            'city': entry['city'],
            'timestamp': entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'weather_forecast': entry['weather_forecast']
        })
    
    return render_template("history.html", history=formatted_history, selected_date=date_str)

@history_bp.route('/history/download')
def download_log():
    filename = request.args.get("file")
    target_path = os.path.join(HISTORY_LOG_DIR, filename)
    if not os.path.isfile(target_path):
        abort(404)
    return send_file(target_path, as_attachment=True)
