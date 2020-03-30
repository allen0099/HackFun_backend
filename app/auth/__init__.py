from flask import Blueprint

auth: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")
bp_callback: Blueprint = Blueprint("callback", __name__, url_prefix="/callback")

from . import callback, google, login
