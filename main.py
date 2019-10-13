import os

from app import create_app, db

FLASK_CONFIG = os.getenv('FLASK_CONFIG')
app = create_app(FLASK_CONFIG or 'default')

# For flask shell debug use
if FLASK_CONFIG == "test":
    @app.shell_context_processor
    def make_shell_context():
        from app.model_test import User, Course, Class
        return dict(db=db, User=User, Course=Course, Class=Class)
elif FLASK_CONFIG == "default":
    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Course, Class, Topic
        return dict(db=db, User=User, Course=Course, Class=Class, Topic=Topic)
