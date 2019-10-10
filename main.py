import configparser

from app import create_app

config = configparser.ConfigParser()
config.read("app/credentials.ini")
FLASK_CONFIG = config["Flask"].get("config")

app = create_app(FLASK_CONFIG or 'default')
