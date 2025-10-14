import unittest
from unittest.mock import patch
from ..app import create_app  # Relative import
from ..services.weather_app_service import WeatherAppService  # Relative impor
from ..utils.weatherutils import WeatherUtil, WeatherForecast, WeatherDay
from ..utils.gpsutils import LocationData

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('weather_app.services.weather_app_service.WeatherAppService.get_weather_forecast')
    def test_home_route(self, mock_get_weather_forecast):
        # Mock the WeatherAppService to return a fake forecast and a location
        fake_forecast = WeatherForecast({
            'date': ['2023-10-01'],
            'minimum_temperture': [15],
            'maximum_temperture': [25],
            'average_humidity': [65]
        }, days=1)
        fake_location = LocationData({
            'latitude': 0,
            'longitude': 0,
            'country': 'IL',
            'name': 'Tel Aviv'
        })
        mock_get_weather_forecast.return_value = (fake_forecast, fake_location)

        # Simulate a POST request to the home route
        response = self.client.post('/', data={'locname': 'Tel Aviv', 'days': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weather Forecast", response.data)
        self.assertIn(b"2023-10-01", response.data)

    @patch('weather_app.services.weather_app_service.WeatherAppService.get_weather_forecast')
    def test_home_route_failure(self, mock_get_weather_forecast):
        # Mock the WeatherAppService to return (None, None) (simulate failure)
        mock_get_weather_forecast.return_value = (None, None)

        # Simulate a POST request to the home route
        response = self.client.post('/', data={'locname': 'Invalid Location', 'days': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed to fetch weather data", response.data)

if __name__ == '__main__':
    unittest.main()
