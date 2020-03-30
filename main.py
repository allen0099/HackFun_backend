import os

from flask import Flask

from app import create_app, db

FLASK_CONFIG: str = os.getenv('FLASK_CONFIG')

app: Flask = create_app(FLASK_CONFIG or "development")


# For flask shell debug use
@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
