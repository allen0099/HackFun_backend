from flask import Flask, make_response, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    from app.authorization.login import login_manager
    login_manager.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    if config_name != "test":
        # import blueprints to flask
        from .api import api as bp_api
        app.register_blueprint(bp_api)
        from .authorization import authorized as bp_authorize
        app.register_blueprint(bp_authorize)
        from .page import edit as bp_page
        app.register_blueprint(bp_page)

    # This allow frontend CORS the resources on this server
    # support_credentials is for cookies allowed
    # TODO should not using wildcard char, replace after production
    CORS(app, origins="*", supports_credentials=True)

    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({
            "error": "Bad request",
            "reason": error.get_description()[3:-4]
        }), 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return make_response(jsonify({
            "error": "Unauthorized",
            "reason": error.get_description()[3:-4],
            "redirect": url_for("login._login", _external=True)
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
