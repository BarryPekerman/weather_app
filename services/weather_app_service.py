from ..utils.gpsutils import LocationUtil
from ..utils.weatherutils import WeatherUtil, WeatherForecast
import logging


#import loggers
from ..app.loggers import event_logger

class WeatherAppService:
    @staticmethod
    def get_weather_forecast(location_name, days):
        """
        Encapsulates the workflow to fetch and parse weather data.
        """
        try:
            # Step 1: Fetch coordinates
            location_util = LocationUtil()
            api_response = location_util.request_coordinates(location_name)
            if not api_response:
                raise ValueError("Failed to fetch coordinates.")
            
            # Step 2: Parse coordinates
            location_data = location_util.parse_coordinates(api_response)
            if location_data.is_empty():
                raise ValueError("Failed to parse coordinates.")
            
            # Step 3: Fetch weather data
            weather_util = WeatherUtil(location_data)
            api_response = weather_util.request_weather(days=days)  # Pass the days parameter here
            if not api_response:
                raise ValueError("Failed to fetch weather data.")
            
            # Step 4: Parse weather data
            parsed_data = weather_util.parse_weather(api_response)
            if not parsed_data:
                raise ValueError("Failed to parse weather data.")
            
            # Step 5: Create weather forecast
            weather_forecast = WeatherForecast(parsed_data, days=days)
            event_logger.info("Weather forecast generated successfully.")
            return weather_forecast, location_data
        
        except Exception as e:
            event_logger.error(f"Error in get_weather_forecast: {e}", exc_info=True)
            return None, None
