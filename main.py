import configparser
import inspect

from flask import Flask

from app import create_app, db, models

config: configparser = configparser.ConfigParser()
config.read("credentials/flask.ini")
FLASK_CONFIG: str = config["Flask"]["config"]

app: Flask = create_app(FLASK_CONFIG or "development")


# For flask shell debug use
@app.shell_context_processor
def make_shell_context() -> dict:
    return dict(
        db=db,
        **dict(
            inspect.getmembers(models, inspect.isclass)
        )
    )
