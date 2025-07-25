from flask import Flask
from .routes import home_bp, history_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(history_bp)
    return app
