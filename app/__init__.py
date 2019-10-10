from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # import blueprints to flask
    from .api import api as bp_api
    app.register_blueprint(bp_api)
    from .authorization import authorized as bp_authorize
    app.register_blueprint(bp_authorize)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.errorhandler(401)
    def unauthorized(error):
        return make_response(jsonify({
            "error": "Unauthorized",
            "reason": error.get_description()[3:-4]
        }), 401)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({
            "error": "Not found",
            "reason": error.get_description()[3:-4]
        }), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({
            "error": "Internal Server Error",
            "reason": error.get_description()[3:-4]
        }), 500)

    return app
