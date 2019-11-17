from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Practice


@api.route("/practice/<string:uuid>")
def root_practice(uuid):
    RESPONSE = {"ok": True}
    practice = Practice.query.filter_by(uuid=uuid).first()

    if not practice:
        RESPONSE["ok"] = False
        RESPONSE["result"] = "Practice not found"
        return jsonify(RESPONSE), 404

    practice_dict = {
        "uuid": practice.uuid,
        "name": practice.name,
        "description": practice.description,
        "hint": [
            {
                "item": hint.item,
                "description": hint.description
            } for hint in practice.hint.all()
        ],
        "type": practice.type,
        "topic": {

        }
    }

    if practice.type == "docker":
        _docker = practice.docker.first()
        if not _docker:
            practice_dict["topic"] = {
                "topic": None,
                "result": "Type Not found!"
            }
        practice_dict["topic"] = {
            "url": _docker.url
        }
    elif practice.type == "choose":
        _choose = practice.choose.first()
        if not _choose:
            practice_dict["topic"] = {
                "topic": None,
                "result": "Type Not found!"
            }
        _append = {
            "multiple": _choose.can_multiple,
            "counts": _choose.choose_count,
            "chooses": {
            }
        }
        _choose_set = {
            "choose1": _choose.chosen_1,
            "choose2": _choose.chosen_2,
            "choose3": _choose.chosen_3,
            "choose4": _choose.chosen_4,
            "choose5": _choose.chosen_5,
            "choose6": _choose.chosen_6,
            "choose7": _choose.chosen_7,
            "choose8": _choose.chosen_8,
            "choose9": _choose.chosen_9,
            "choose10": _choose.chosen_10
        }
        i = _choose.choose_count
        for j in range(10 - i):
            _choose_set.popitem()
        _append["chooses"] = _choose_set
        practice_dict["topic"] = _append
    else:
        practice_dict["topic"] = {
            "topic": None,
            "result": "Type Error!"
        }
    RESPONSE["practice"] = practice_dict
    return jsonify(RESPONSE)


@api.route("/practice/<string:uuid>/")
def redirect_practice(uuid):
    return redirect(url_for("api.root_practice", uuid=uuid))
