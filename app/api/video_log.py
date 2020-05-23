from flask import Response, session, make_response, jsonify, request
from flask_login import login_required

from app.api import api
from app.models import VidRecord


@api.route("/vid_log", methods=["POST"])
@login_required
def root_vid_log() -> Response:
    uid: str = session.get("_user_id") or session.get("user_id")
    response: dict = {
        "ok": True,
        "uid": uid
    }

    input_data: dict = request.json or dict()
    if _chk_input(input_data):
        post_id, post_time, post_progress = input_data["id"], input_data["time"], input_data["progress"]
    else:
        response["result"] = "Parameters missing!"
        return make_response(jsonify(response), 400)

    record: VidRecord = VidRecord.query \
        .filter_by(user_id=uid) \
        .filter_by(lesson_id=post_id).first()

    if record is None:
        VidRecord.add(uid, post_id, post_progress, post_time)
    else:
        record.update(post_progress, post_time)

    response["result"]: str = "Success!"

    return make_response(jsonify(response))


def _chk_input(_: dict) -> bool:
    if _.get("id", None) in [None, ""]:
        return False
    if _.get("time", None) in [None, ""]:
        return False
    if _.get("progress", None) in [None, ""]:
        return False
    return True
