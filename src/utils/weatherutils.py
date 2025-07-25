import requests
from ..utils.gpsutils import LocationData
import logging

#import loggers
from ..app.loggers import event_logger

class WeatherForecast:
    """
    Obj to contain multiple weather days, to be able to iterate over them.
    """
    def __init__(self, data=None, days=0):
        self.days = int(days)
        self.weather = []
        if data:
            # Ensure we don't exceed the available data
            available_days = len(data.get('date', []))  # Get all available days from the API response
            # Process up to the requested days or available days
            for index in range(min(self.days, available_days)):
                self.weather.append(WeatherDay(data, index))
            event_logger.info(f"Processing {min(self.days, available_days)} days out of {available_days} available.")
    
    def __iter__(self):
        for day in self.weather:
            yield day
        
    def __repr__(self):
        return self.weather.__repr__()
    
    def is_empty(self):
        return len(self.weather) == 0

    def to_dict(self):
        """Convert the weather forecast to a dictionary for MongoDB storage"""
        return {
            'days': self.days,
            'weather': [{
                'date': day.date,
                'minimum_temperature': day.minimum_temperture,
                'maximum_temperature': day.maximum_temperture,
                'average_humidity': day.average_humidity
            } for day in self.weather]
        }

class WeatherDay:
    """
    Order weather information into day objects
    Initialize a day object with parsed weather data from WeatherInfoParser object
    Second arg indicates which day it is in the WeatherInfoParser object 
    """
    def __init__(self, data={}, index=0):
        event_logger.info(f'weather data: {data}')
        self.date = None if 'date' not in data else (None if data['date'] is None else data.get('date')[index])
        self.minimum_temperture = None if 'minimum_temperture' not in data else (None if data['minimum_temperture'] is None else data.get('minimum_temperture')[index])
        self.maximum_temperture = None if 'maximum_temperture' not in data else (None if data['maximum_temperture'] is None else data.get('maximum_temperture')[index])
        self.average_humidity = None if 'average_humidity' not in data else (None if data['average_humidity'] is None else data.get('average_humidity')[index])
	
    def __repr__(self):
        return f"date: {self.date}, minimum_temperture: {self.minimum_temperture}, maximum_temperture: {self.maximum_temperture}, average_humidity: {self.average_humidity}"
	
    def is_empty(self):
        """check if day is not initialized properly.
        if it is empty or invalid, return true. 
        if it has data, return false"""
        if not self.date or not self.minimum_temperture or not self.maximum_temperture or not self.average_humidity:
            return True
        return False


class WeatherUtil:
    """
    Handles parsing info from response json on weather info
    into requested human readable information.
    """
    def __init__(self, location_data):
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            'longitude': None,
            'latitude': None,
            'forecast_days': None,
            'hourly': ['relative_humidity_2m'],
            'daily': ['temperature_2m_max', 'temperature_2m_min']
        }
        self.data_parsed = {}
        if location_data:
            self.params['longitude'] = location_data.get_longitude()
            self.params['latitude'] = location_data.get_latitude()

    def request_weather(self, days):
        """
        Makes an API request to fetch weather data.
        """
        # Update the forecast_days parameter with the requested number of days
        self.params['forecast_days'] = days
        try:
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()
            event_logger.info(f"Weather API request successful. Requested {days} days.")
            return response.json()
        except requests.exceptions.RequestException as e:
            event_logger.error(f"Weather API request failed: {e}", exc_info=True)
            return None

    def parse_weather(self, api_response):
        """
        Parses the API response into a dictionary for WeatherForecast.
        """
        if not api_response:
            event_logger.error("No data found in weather API response.")
            return None
        
        try:
            data_parsed = {
                'date': api_response['daily']['time'],
                'minimum_temperture': api_response['daily']['temperature_2m_min'],
                'maximum_temperture': api_response['daily']['temperature_2m_max'],
                'average_humidity': self.calculate_average_humidity(api_response['hourly']['relative_humidity_2m'])
            }
            event_logger.info(f"Successfully parsed weather API response. Found {len(data_parsed['date'])} days of data.")
            return data_parsed
        except KeyError as e:
            event_logger.error(f"Failed to parse weather API response: {e}", exc_info=True)
            return None

    def calculate_average_humidity(self, hourly_humidity):
        """
        Calculates the average humidity for each day.
        """
        hours_in_day = 24
        days = len(hourly_humidity) // hours_in_day
        average_humidity = [sum(hourly_humidity[i * hours_in_day:(i + 1) * hours_in_day]) // hours_in_day for i in range(days)]
        return average_humidity
