import time
from typing import List

from flask import jsonify, make_response, Response, request, session, redirect, url_for
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Practice, Choose, Complete


@api.route("/choose", methods=["POST"])
def root_choose() -> Response:
    if current_user.is_authenticated:
        response: dict = {
            "ok": False,
            "result": "Check your parameters and try again!"
        }
        uid: str = session.get("_user_id") or session.get("user_id")

        input_data: dict = request.json or dict()

        if _chk_input(input_data):
            input_id: str = input_data["id"]
            submitted_ids: List[int] = input_data.get("choose")
        else:
            response["result"] = "Parameters missing!"
            return make_response(jsonify(response), 400)

        practice: Practice = Practice.query.filter_by(id=input_id).first_or_404()
        choose: Choose = practice.choose.first_or_404()

        submitted_ids.sort()
        correct_ids: List[int] = [option.id for option in choose.option.filter_by(is_ans=True).all()]

        if correct_ids == submitted_ids:
            if not Complete.is_solved(uid, practice.uuid):
                response["ok"] = True
                response["result"] = "Success! You had submitted the correct answer!"
                Complete.add(uid, practice.uuid)
            else:
                response["ok"] = True
                response["result"] = "You had submitted the answer!"
        else:
            response["ok"] = False
            response["result"] = "Wrong choice, check the choice and try again!"
        response["time"] = int(time.time())

        return make_response(jsonify(response))
    else:
        return login_manager.unauthorized()


@api.route("/choose/", methods=["POST"])
def redirect_root_choose() -> redirect:
    return redirect(url_for("api.root_choose"))


def _chk_input(_: dict) -> bool:
    if _.get("id", None) in [None, ""]:
        return False
    if _.get("choose", None) in [None, ""]:
        return False
    return True
