# TODO avoid replay attack
#   https://github.com/mbr/flask-kvsession
import time

from flask import jsonify, make_response, Response, redirect, url_for, request
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Flag


@api.route("/flag", methods=["POST"])
def root_flag() -> Response:
    if current_user.is_authenticated:
        RESPONSE: dict = {
            "ok": False,
            "result": ""
        }
        content: dict = request.json or dict()
        if content.get("flag", None) == None:
            RESPONSE["result"] = "Flag missing!"
            return make_response(jsonify(RESPONSE), 400)
        else:
            post_flag: str = content["flag"]
        if content.get("uuid") == None:
            RESPONSE["result"] = "UUID missing!"
            return make_response(jsonify(RESPONSE), 400)
        else:
            post_uuid: str = content["uuid"]

        flag: Flag = Flag.query.filter_by(flag=post_flag).first()
        if flag is None or post_uuid != flag.docker.practice.uuid:
            RESPONSE["result"] = "Invalid data!"
            return make_response(jsonify(RESPONSE), 404)
        else:
            RESPONSE["ok"] = True
            RESPONSE["result"] = "Valid data!"
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
