from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Lesson


@api.route("/lesson/<string:name>")
def root_lesson(name) -> jsonify:
    RESPONSE: dict = {"ok": False}
    lesson: Lesson = Lesson.query.filter_by(name=name).first()

    if not lesson:
        RESPONSE["result"]: str = "Lesson not found"
        return jsonify(RESPONSE), 404

    RESPONSE["ok"]: bool = True
    RESPONSE["lesson"]: dict = {
        "id": lesson.id,
        "name": lesson.name,
        "description": lesson.description,
        "url": lesson.url,
        "practices": [
            {
                "name": practice.name,
                "description": practice.description,
                "uuid": practice.uuid
            } for practice in lesson.practices.all()
        ]
    }

    return jsonify(RESPONSE)


@api.route("/lesson/<string:name>/")
def redirect_lesson(name) -> redirect:
    return redirect(url_for("api.root_lesson", name=name))
