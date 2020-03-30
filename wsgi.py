import configparser

from flask import Flask

from app import create_app

config: configparser.ConfigParser = configparser.ConfigParser()
config.read("credentials/flask.ini")
FLASK_CONFIG: str = config["Flask"]["config"]

application: Flask = create_app(FLASK_CONFIG)
