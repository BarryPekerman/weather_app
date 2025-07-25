import unittest
from ..utils.weatherutils import WeatherUtil, WeatherForecast, WeatherDay
from ..utils.gpsutils import LocationData

class TestWeatherDay(unittest.TestCase):
    def test_weather_day_initialization(self):
        data = {
            "date": ["2025-01-26"],
            "minimum_temperture": [5.0],
            "maximum_temperture": [10.0],
            "average_humidity": [80]
        }
        weather_day = WeatherDay(data, 0)
        self.assertEqual(weather_day.date, "2025-01-26")
        self.assertEqual(weather_day.minimum_temperture, 5.0)
        self.assertEqual(weather_day.maximum_temperture, 10.0)
        self.assertEqual(weather_day.average_humidity, 80)

    def test_weather_day_is_empty(self):
        empty_weather_day = WeatherDay()
        self.assertTrue(empty_weather_day.is_empty())

class TestWeatherForecast(unittest.TestCase):
    def test_weather_forecast_initialization(self):
        data = {
            "date": ["2025-01-26", "2025-01-27"],
            "minimum_temperture": [5.0, 6.0],
            "maximum_temperture": [10.0, 11.0],
            "average_humidity": [80, 85]
        }
        weather_forecast = WeatherForecast(data, days=2)
        self.assertEqual(len(weather_forecast.weather), 2)
        self.assertEqual(weather_forecast.weather[0].date, "2025-01-26")
        self.assertEqual(weather_forecast.weather[1].date, "2025-01-27")

    def test_weather_forecast_is_empty(self):
        empty_forecast = WeatherForecast()
        self.assertTrue(empty_forecast.is_empty())

class TestWeatherUtil(unittest.TestCase):
    def setUp(self):
        self.location_data = LocationData({
            "latitude": 51.5085,
            "longitude": -0.1257,
            "country": "UK",
            "name": "London"
        })

    def test_request_weather_success(self):
        weather_util = WeatherUtil(self.location_data)
        response = weather_util.request_weather(days=7)
        self.assertIsNotNone(response)
        self.assertIn("daily", response)

    def test_parse_weather_success(self):
        weather_util = WeatherUtil(self.location_data)
        api_response = {
            "daily": {
                "time": ["2025-01-26", "2025-01-27"],
                "temperature_2m_min": [5.0, 6.0],
                "temperature_2m_max": [10.0, 11.0]
            },
            "hourly": {
                "relative_humidity_2m": [80] * 48  # 2 days of hourly data
            }
        }
        parsed_data = weather_util.parse_weather(api_response)
        self.assertIsNotNone(parsed_data)
        self.assertEqual(len(parsed_data["date"]), 2)

if __name__ == "__main__":
    unittest.main()
