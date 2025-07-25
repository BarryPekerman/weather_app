import os
from weather_app.app import create_app

APP_PORT = os.getenv("APP_PORT", "5000")

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=APP_PORT)
