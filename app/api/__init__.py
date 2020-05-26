from flask import Blueprint

api: Blueprint = Blueprint("api", __name__, url_prefix="/api")

from . import choose
from . import course
from . import download
from . import flag
from . import lesson
from . import profile
from . import tab
from . import video_log
