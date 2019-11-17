from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Lesson


@api.route("/lesson/<string:name>")
def root_lesson(name):
    RESPONSE = {"ok": False}
    lesson = Lesson.query.filter_by(name=name).first()

    if not lesson:
        RESPONSE["result"] = "Lesson not found"
        return jsonify(RESPONSE), 404

    RESPONSE["ok"] = True
    RESPONSE["lesson"] = {
        "name": lesson.name,
        "description": lesson.description,
        "url": lesson.url,
        "practices": [
            {
                "name": practice.name,
                "description": practice.description,
            } for practice in lesson.practices.all()
        ]
    }

    return jsonify(RESPONSE)


@api.route("/lesson/<string:name>/")
def redirect_lesson(name):
    return redirect(url_for("api.root_lesson", name=name))
