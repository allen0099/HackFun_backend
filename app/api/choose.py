import time
from typing import List

from flask import jsonify, make_response, Response, request
from flask_login import current_user

from app import login_manager
from app.api import api
from app.models import Practice, Choose, Option


@api.route("/choose/<int:practice_id>", methods=["POST"])
def root_choose(practice_id) -> Response:
    practice: Practice = Practice.query.filter_by(id=practice_id).first()
    choose: Choose = practice.choose.first_or_404()
    if current_user.is_authenticated:
        response: dict = {
            "ok": False,
            "result": "Check your parameters and try again!"
        }

        options: List[Option] = choose.option.filter_by(is_ans=True).all()
        submitted: dict = request.json
        correct_ids: List[int] = [option.id for option in options]
        submitted_ids: List[int] = submitted.get("choose")
        if correct_ids == submitted_ids:
            response["ok"] = True
            response["result"] = "Success! You had submitted the correct answer!"
        else:
            response["ok"] = False
            response["result"] = "Wrong choice, check the choice and try again!"
        response["time"] = int(time.time())
        # TODO user check
        # TODO time record
        # TODO has done check
        return make_response(jsonify(response))
    else:
        return login_manager.unauthorized()
