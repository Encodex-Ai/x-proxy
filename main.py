from flask import Flask
from api import api_bp
from config import Config
from services.x_service import XService
from services.oauth_setup import setup_and_validate_oauth
from services.combined_services import CombinedServices
from error_handlers import register_error_handlers
from services.mongodb_service import MongoDBService
from typing import Type


def create_app(config_class: Type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    oauth2_handler, oauth1_handler = setup_and_validate_oauth(app.config)

    oauth2_handler.start_refresh_thread()

    x_service = XService(oauth2_handler, oauth1_handler.api)
    app.x_service = x_service

    mongodb_service = MongoDBService(app.config)
    app.mongodb_service = mongodb_service

    combined_services = CombinedServices(mongodb_service, x_service, app.config)
    app.combined_services = combined_services

    app.register_blueprint(api_bp, url_prefix="/api")

    # Register error handlers
    register_error_handlers(app)

    @app.route("/")
    def hello() -> str:
        return "Greetings, your pseudo-X-API is up and running!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4000)
