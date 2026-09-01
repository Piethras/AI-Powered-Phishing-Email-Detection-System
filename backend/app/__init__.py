"""
Flask application factory.

This is the ORCHESTRATION layer of the 3-tier architecture:
Raw email -> Parser -> Feature modules -> Classifier -> (this layer) -> MySQL -> React

Flask does not store data long-term (that's MySQL's job) and does not render
UI (that's React's job) - it receives requests, runs the analysis pipeline,
and returns/persists results.
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)  # allow the React frontend (different origin) to call this API
    db.init_app(app)

    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
