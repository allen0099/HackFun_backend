from flask import jsonify, Response
from flask_login import login_required, logout_user, current_user

from app import login_manager
from app.auth import auth
from app.models import User


@login_manager.user_loader
def load_user(uid) -> User:
    # User object return, not str
    return User.get(uid)


@auth.route("/user")
@login_required
def _user() -> Response:
    RESPONSE: dict = {
        "ok": True,
        "result": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "pic": current_user.profile_pic
        }
    }
    return jsonify(RESPONSE)


@auth.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    RESPONSE: dict = {
        "ok": True,
        "result": "logout success!"
    }
    return jsonify(RESPONSE)
