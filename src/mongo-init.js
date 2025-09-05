// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to the weather database
db = db.getSiblingDB('weather');

// Create a user for the weather application
db.createUser({
  user: 'weather_user',
  pwd: 'WeatherApp2025!',
  roles: [
    {
      role: 'readWrite',
      db: 'weather'
    }
  ]
});

// Create the search_history collection
db.createCollection('search_history');

// Create an index on timestamp for better query performance
db.search_history.createIndex({ "timestamp": -1 });

// Create an index on city for city-based queries
db.search_history.createIndex({ "city": 1 });

// Insert a sample document to verify the setup
db.search_history.insertOne({
  city: "Sample City",
  timestamp: new Date(),
  weather_forecast: {
    message: "Database initialized successfully"
  }
});

print("MongoDB weather database initialized successfully!"); 