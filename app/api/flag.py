import time

from flask import jsonify, make_response, Response, redirect, url_for, request, session
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Flag, Complete, Practice


@api.route("/flag", methods=["POST"])
def root_flag() -> Response:
    if current_user.is_authenticated:
        response: dict = {
            "ok": False,
            "result": ""
        }
        uid: str = session.get("_user_id") or session.get("user_id")

        input_data: dict = request.json or dict()

        if _chk_input(input_data):
            post_flag, post_id = input_data["flag"], input_data["id"]
        else:
            response["result"] = "Parameters missing!"
            return make_response(jsonify(response), 400)

        flag: Flag = Flag.query.filter_by(flag=post_flag).first()
        practice: Practice = Practice.query.filter_by(id=post_id).first()

        if flag is None or practice.uuid != flag.docker.practice.uuid:
            response["result"] = "Failed! Wrong flag submitted!"
            return make_response(jsonify(response), 404)
        else:
            response["ok"] = True
            if not Complete.is_solved(uid, practice.uuid):
                response["result"] = "Success!"
                Complete.add(uid, practice.uuid)
            else:
                response["result"] = "You had submitted the answer!"
        response["time"] = int(time.time())

        return make_response(jsonify(response))
    else:
        return login_manager.unauthorized()


@api.route("/flag/", methods=["POST"])
def redirect_root_flag() -> redirect:
    return redirect(url_for("api.root_flag"))


def _chk_input(_: dict) -> bool:
    if _.get("flag", None) in [None, ""]:
        return False
    if _.get("id", None) in [None, ""]:
        return False
    return True
