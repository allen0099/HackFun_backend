import time
from typing import List

from flask import jsonify, make_response, Response, request, session
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Practice, Choose, Option, Complete


@api.route("/choose/<int:practice_id>", methods=["POST"])
def root_choose(practice_id) -> Response:
    practice: Practice = Practice.query.filter_by(id=practice_id).first()
    choose: Choose = practice.choose.first_or_404()
    if current_user.is_authenticated:
        response: dict = {
            "ok": False,
            "result": "Check your parameters and try again!"
        }
        uid: str = session.get("_user_id") or session.get("user_id")

        options: List[Option] = choose.option.filter_by(is_ans=True).all()
        submitted: dict = request.json
        correct_ids: List[int] = [option.id for option in options]
        submitted_ids: List[int] = submitted.get("choose")
        if correct_ids == submitted_ids:
            response["ok"] = True
            response["result"] = "Success! You had submitted the correct answer!"

            Complete.add(uid, practice.uuid)
        else:
            response["ok"] = False
            response["result"] = "Wrong choice, check the choice and try again!"
        response["time"] = int(time.time())

        return make_response(jsonify(response))
    else:
        return login_manager.unauthorized()
