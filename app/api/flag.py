import time

from flask import jsonify, make_response, Response, redirect, url_for, request, session
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Flag, Complete


@api.route("/flag", methods=["POST"])
def root_flag() -> Response:
    if current_user.is_authenticated:
        response: dict = {
            "ok": False,
            "result": ""
        }
        uid: str = session.get("_user_id") or session.get("user_id")

        content: dict = request.json or dict()

        if _chk_input(content):
            post_flag, post_uuid = content["flag"], content["uuid"]
        else:
            response["result"] = "Parameters missing!"
            return make_response(jsonify(response), 400)

        flag: Flag = Flag.query.filter_by(flag=post_flag).first()
        if flag is None or post_uuid != flag.docker.practice.uuid:
            response["result"] = "Failed! Wrong flag submitted!"
            return make_response(jsonify(response), 404)
        else:
            response["ok"] = True
            if not Complete.is_solved(uid, post_uuid):
                response["result"] = "Success!"
                Complete.add(uid, post_uuid)
            else:
                response["result"] = "You had submitted the answer!"
        response["time"] = int(time.time())

        return make_response(jsonify(response))
    else:
        return login_manager.unauthorized()


@api.route("/flag/", methods=["POST"])
def redirect_root_flag() -> redirect:
    return redirect(url_for("api.root_flag"))


def _chk_input(content: dict) -> bool:
    if content.get("flag", None) is None:
        return False
    if content.get("uuid", None) is None:
        return False
    return True
