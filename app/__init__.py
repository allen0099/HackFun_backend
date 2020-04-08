from flask import Flask, make_response, jsonify, url_for, Response
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db: SQLAlchemy = SQLAlchemy()

login_manager: LoginManager = LoginManager()

# TODO build docker

# TODO remove .idea from git
def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    CORS(app, origins="*", supports_credentials=True)

    from .api import api as bp_api
    app.register_blueprint(bp_api)
    from .auth import auth as bp_auth
    app.register_blueprint(bp_auth)
    from .auth import bp_callback
    app.register_blueprint(bp_callback)

    from .page import edit as bp_page
    app.register_blueprint(bp_page)

    @app.errorhandler(400)
    def bad_request(error) -> Response:
        return make_response(jsonify({
            "error": "Bad request",
            "reason": error.get_description()[3:-4]
        }), 400)

    @app.errorhandler(401)
    def unauthorized(error) -> Response:
        return make_response(jsonify({
            "error": "Unauthorized",
            "reason": error.get_description()[3:-4],
            "redirect": url_for("auth._login", _external=True)
        }), 401)

    @app.errorhandler(404)
    def not_found(error) -> Response:
        return make_response(jsonify({
            "error": "Not found",
            "reason": error.get_description()[3:-4]
        }), 404)

    @app.errorhandler(500)
    def internal_server_error(error) -> Response:
        return make_response(jsonify({
            "error": "Internal Server Error",
            "reason": error.get_description()[3:-4]
        }), 500)

    return app
