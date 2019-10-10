from flask import Blueprint

authorized = Blueprint("login", __name__)

from . import login
