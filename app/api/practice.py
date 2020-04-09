from flask import jsonify, make_response, Response, redirect, url_for, abort

from app.api import api
from app.models import Practice


@api.route("/practice")
def root_practice() -> Response:
    RESPONSE: dict = {
        "ok": False,
        "result": "practice uuid is empty!"
    }
    return make_response(jsonify(RESPONSE), 400)


@api.route("/practice/")
def redirect_root_practice() -> redirect:
    return redirect(url_for("api.root_practice"))


@api.route("/practice/<uuid:uuid>")
def search_practice(uuid) -> Response:
    RESPONSE: dict = dict()
    practice: Practice = Practice.query.filter_by(uuid=uuid).first()

    if not practice:
        RESPONSE["ok"]: bool = False
        RESPONSE["result"]: str = "Practice not found"
        return make_response(jsonify(RESPONSE), 404)

    RESPONSE["ok"]: bool = True
    RESPONSE["practice"]: dict = {
        "id": practice.id,
        "uuid": practice.uuid,
        "name": practice.name,
        "type": practice.type
    }

    if practice.type == "choose":
        RESPONSE["practice"]["questions"]: list = [
            {
                "statement": question.desc,
                "options": [
                    {
                        "id": option.id,
                        "value": option.desc
                    } for option in question.options.all()
                ]
            } for question in practice.question.all()
        ]
    elif practice.type == "docker":
        RESPONSE["practice"]["docker"]: list = [
            {
                "statement": docker.desc,
                "url": docker.url
            } for docker in practice.docker.all()
        ]
    else:
        return make_response(abort(500, "Practice type undefined!"))
    RESPONSE["practice"]["hints"]: list = [
        hint.desc for hint in practice.hint.all()
    ]
    return make_response(jsonify(RESPONSE))


@api.route("/practice/<uuid:uuid>/")
def redirect_practice(uuid) -> redirect:
    return redirect(url_for("api.search_practice", uuid=uuid))
