from flask import Flask, make_response, jsonify, url_for, Response
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.config import config
from app.misc.binarychecker import BinaryChecker

db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager()
binary_check: BinaryChecker = BinaryChecker()


# TODO https://github.com/mbr/flask-kvsession
def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    binary_check.init_app(app)

    CORS(app, origins="*", supports_credentials=True)

    from .api import api as bp_api
    app.register_blueprint(bp_api)
    from .auth import auth as bp_auth
    app.register_blueprint(bp_auth)
    from .auth import bp_callback
    app.register_blueprint(bp_callback)

    @app.errorhandler(400)
    def bad_request(error) -> Response:
        return make_response(jsonify({
            "error": "Bad Request",
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
            "error": "Not Found",
            "reason": error.get_description()[3:-4]
        }), 404)

    @app.errorhandler(405)
    def not_found(error) -> Response:
        return make_response(jsonify({
            "error": "Method Not Allowed",
            "reason": error.get_description()[3:-4]
        }), 405)

    @app.errorhandler(500)
    def internal_server_error(error) -> Response:
        return make_response(jsonify({
            "error": "Internal Server Error",
            "reason": error.get_description()[3:-4]
        }), 500)

    return app
