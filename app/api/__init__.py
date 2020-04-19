from flask import Blueprint

api: Blueprint = Blueprint("api", __name__, url_prefix="/api")

from . import tab, course, lesson, post
