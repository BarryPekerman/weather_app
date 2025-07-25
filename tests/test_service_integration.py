import unittest
from unittest.mock import patch, MagicMock
import importlib

# Dynamically import the modules using relative paths
gpsutils = importlib.import_module('weather_app.utils.gpsutils', package='..tests')#TODO: FIX
weatherutils = importlib.import_module('weather_app.utils.weatherutils', package='..tests')#TODO: FIX

# Import the service and data classes
from ..services.weather_app_service import WeatherAppService  # Relative import
from ..utils.gpsutils import LocationData  # Relative import

class TestWeatherAppServiceIntegration(unittest.TestCase):
    @patch.object(gpsutils.LocationUtil, 'request_coordinates')  # Relative path
    @patch.object(weatherutils.WeatherUtil, 'request_weather')  # Relative path
    def test_get_weather_forecast_success(self, mock_request_weather, mock_request_coordinates):
        # Mock the LocationUtil.request_coordinates response
        mock_request_coordinates.return_value = {
            "results": [
                {
                    "latitude": 51.5085,
                    "longitude": -0.1257,
                    "country": "UK",
                    "name": "London"
                }
            ]
        }

        # Mock the WeatherUtil.request_weather response
        mock_request_weather.return_value = {
            "daily": {
                "time": ["2025-01-26", "2025-01-27"],
                "temperature_2m_min": [5.0, 6.0],
                "temperature_2m_max": [10.0, 11.0]
            },
            "hourly": {
                "relative_humidity_2m": [80] * 48  # 2 days of hourly data
            }
        }

        # Call the method under test
        location_name = "London"
        days = 2
        weather_forecast = WeatherAppService.get_weather_forecast(location_name, days)

        # Assertions
        self.assertIsNotNone(weather_forecast)
        self.assertEqual(len(weather_forecast.weather), 2)
        self.assertEqual(weather_forecast.weather[0].date, "2025-01-26")
        self.assertEqual(weather_forecast.weather[1].date, "2025-01-27")

    @patch.object(gpsutils.LocationUtil, 'request_coordinates')  # Relative path
    def test_get_weather_forecast_failure_invalid_location(self, mock_request_coordinates):
        # Mock the LocationUtil.request_coordinates response for an invalid location
        mock_request_coordinates.return_value = None

        # Call the method under test
        location_name = "InvalidLocationName"
        days = 7
        weather_forecast = WeatherAppService.get_weather_forecast(location_name, days)

        # Assertions
        self.assertIsNone(weather_forecast)

    @patch.object(gpsutils.LocationUtil, 'request_coordinates')  # Relative path
    @patch.object(weatherutils.WeatherUtil, 'request_weather')  # Relative path
    def test_get_weather_forecast_failure_invalid_days(self, mock_request_weather, mock_request_coordinates):
        # Mock the LocationUtil.request_coordinates response
        mock_request_coordinates.return_value = {
            "results": [
                {
                    "latitude": 51.5085,
                    "longitude": -0.1257,
                    "country": "UK",
                    "name": "London"
                }
            ]
        }

        # Mock the WeatherUtil.request_weather response for invalid days
        mock_request_weather.return_value = None

        # Call the method under test
        location_name = "London"
        days = -1  # Invalid number of days
        weather_forecast = WeatherAppService.get_weather_forecast(location_name, days)

        # Assertions
        self.assertIsNone(weather_forecast)

if __name__ == "__main__":
    unittest.main()
