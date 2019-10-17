import os

from app import create_app, db

FLASK_CONFIG = os.getenv('FLASK_CONFIG')
app = create_app(FLASK_CONFIG or 'default')


# For flask shell debug use
@app.shell_context_processor
def make_shell_context():
    from app.models import User, Course, Class, Topic, TopicChoose, TopicDocker
    return dict(db=db, User=User, Course=Course, Class=Class, Topic=Topic, TopicChoose=TopicChoose
                , TopicDocker=TopicDocker)
