import configparser

from app import create_app, db
from app.models import User, Course, Class, Topic

config = configparser.ConfigParser()
config.read("credentials.ini")
FLASK_CONFIG = config["Flask"].get("config")

app = create_app(FLASK_CONFIG or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Course=Course, Class=Class, Topic=Topic)
