import requests
import logging

#import loggers
from ..app.loggers import event_logger

class LocationData:
    """
    Obj containing information on location.
    """
    def __init__(self, data={"latitude": None, "longitude": None, "country": None, "name": None}):
        self.latitude = data.get("latitude")
        self.longitude = data.get("longitude")
        self.country = data.get("country")
        self.name = data.get("name")

    def get_latitude(self):
        return float(self.latitude)

    def get_longitude(self):
        return float(self.longitude)

    def get_country(self):
        return str(self.country)

    def get_name(self):
        return str(self.name)

    def is_empty(self):
        """
        Returns True if object is empty, else False.
        """
        if not self.latitude or not self.longitude or not self.country or not self.name:
            event_logger.info(f"self.latitude: {self.latitude} --- {not self.latitude or not self.longitude or not self.country or not self.name}", exc_info=True)

            return True
        return False

    def __repr__(self):
        return f"Location: latitude:{self.latitude}, longitude:{self.longitude}, country:{self.country}, name:{self.name}"

class LocationUtil:
    """
    Gets geo-location coordinates for a given location name, can add a country for specific results.
    Returns dictionary with information defined the initialization of this class.
    """
    def __init__(self, keys=("latitude", "longitude", "country", "name")):
        self.url = "https://geocoding-api.open-meteo.com/v1/search"
        self.parse_keys = keys

    def request_coordinates(self, name="haifa", country=None, results=1):
        """
        Makes an API request to fetch coordinates for a given location name.
        """
        event_logger.info(f"COORDINATES START: {name}", exc_info=True)
        if country:
            name = name + "," + country
        self.params = {'name': name, 'count': results, 'language': 'en', 'format': 'json'}
        try:
            event_logger.info(f"COORDINATES: {name}", exc_info=True)

            response = requests.get(self.url, params=self.params)
            event_logger.info(f"RESPONSE: {response.text}", exc_info=True)
            if len(response.json()) == 1:
                event_logger.error(f"RESPONSE BAD BODY: {response.text}", exc_info=True)
                return None
            response.raise_for_status()
            event_logger.info(f"API request successful for location: {name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            event_logger.error(f"API request failed: {e}", exc_info=True)
            return None


    def parse_coordinates(self, api_response):
        """
        Parses the API response into a LocationData object.
        """
        if not api_response or 'results' not in api_response or len(api_response['results']) == 0:
            event_logger.error("No data found in API response.")
            return LocationData()

        data = api_response['results'][0]
        GPS = LocationData({key: data[key] for key in self.parse_keys})
        if GPS.is_empty():
            event_logger.error("Failed to parse API response into LocationData.")
            return LocationData()

        event_logger.info("Successfully parsed API response into LocationData.")
        return GPS
