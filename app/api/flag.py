# TODO avoid replay attack
#   https://github.com/mbr/flask-kvsession
import time

from flask import jsonify, make_response, Response, redirect, url_for, request, session
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Flag


@api.route("/flag", methods=["POST"])
def root_flag() -> Response:
    if current_user.is_authenticated:
        RESPONSE: dict = {
            "ok": False,
            "result": "Check your parameters and try again!"
        }
        content: dict = request.json
        if content.get("flag") == None:
            return make_response(jsonify(RESPONSE), 400)

        flag: Flag = Flag.query.filter_by(flag=content.get("flag")).first()
        if flag is None:
            return make_response(jsonify(RESPONSE), 404)
        else:
            RESPONSE["ok"] = True
            RESPONSE["result"] = "Flag submitted!"
        RESPONSE["time"] = int(time.time())
        # TODO user check
        # TODO time record
        # TODO has done check
        # uid = session.get("_user_id")

        return make_response(jsonify(RESPONSE))
    else:
        return login_manager.unauthorized()


@api.route("/flag/", methods=["POST"])
def redirect_root_flag() -> redirect:
    return redirect(url_for("api.root_flag"))
