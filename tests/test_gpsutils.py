import unittest
from ..utils.gpsutils import LocationUtil, LocationData

class TestLocationData(unittest.TestCase):
    def test_location_data_initialization(self):
        data = {
            "latitude": 51.5085,
            "longitude": -0.1257,
            "country": "UK",
            "name": "London"
        }
        location = LocationData(data)
        self.assertEqual(location.get_latitude(), 51.5085)
        self.assertEqual(location.get_longitude(), -0.1257)
        self.assertEqual(location.get_country(), "UK")
        self.assertEqual(location.get_name(), "London")

    def test_location_data_is_empty(self):
        empty_location = LocationData()
        self.assertTrue(empty_location.is_empty())

        non_empty_location = LocationData({"latitude": 51.5085})
        self.assertTrue(non_empty_location.is_empty())

class TestLocationUtil(unittest.TestCase):
    def test_request_coordinates_success(self):
        location_util = LocationUtil()
        response = location_util.request_coordinates("London")
        self.assertIsNotNone(response)
        self.assertIn("results", response)

    def test_request_coordinates_failure(self):
        location_util = LocationUtil()
        response = location_util.request_coordinates("InvalidLocationName")
        self.assertIsNone(response)

    def test_parse_coordinates_success(self):
        location_util = LocationUtil()
        api_response = {
            "results": [
                {
                    "latitude": 51.5085,
                    "longitude": -0.1257,
                    "country": "UK",
                    "name": "London"
                }
            ]
        }
        location_data = location_util.parse_coordinates(api_response)
        self.assertFalse(location_data.is_empty())
        self.assertEqual(location_data.get_latitude(), 51.5085)
        self.assertEqual(location_data.get_longitude(), -0.1257)

    def test_parse_coordinates_failure(self):
        location_util = LocationUtil()
        api_response = {}  # Empty response
        location_data = location_util.parse_coordinates(api_response)
        self.assertTrue(location_data.is_empty())

if __name__ == "__main__":
    unittest.main()
