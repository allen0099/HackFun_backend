import os

from app import create_app, db

FLASK_CONFIG = os.getenv('FLASK_CONFIG')
app = create_app(FLASK_CONFIG or 'default')


# For flask shell debug use
@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
