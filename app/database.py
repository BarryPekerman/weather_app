from pymongo import MongoClient
from datetime import datetime, timezone
import os

class MongoDBService:
    def __init__(self):
        # Get MongoDB connection details from environment variables
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        self.client = MongoClient(mongo_uri)
        self.db = self.client.weather
        self.history = self.db.search_history

    def save_search(self, city, weather_forecast):
        """Save a search to MongoDB"""
        document = {
            'city': city,
            'timestamp': datetime.now(timezone.utc),
            'weather_forecast': weather_forecast.to_dict()
        }
        return self.history.insert_one(document)

    def get_search_history(self, limit=100):
        """Get recent search history"""
        return list(self.history.find().sort('timestamp', -1).limit(limit))

    def get_search_history_by_date(self, date):
        """Get search history for a specific date"""
        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())
        return list(self.history.find({
            'timestamp': {
                '$gte': start_date,
                '$lte': end_date
            }
        }).sort('timestamp', -1)) 