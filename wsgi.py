import configparser

from app import create_app

config = configparser.ConfigParser()
config.read("credentials.ini")
FLASK_CONFIG = config["Flask"]["config"]

application = create_app(FLASK_CONFIG)
