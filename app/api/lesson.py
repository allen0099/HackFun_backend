from flask import jsonify, make_response, Response, redirect, url_for

from app.api import api
from app.models import Lesson


@api.route("/lesson")
def root_lesson() -> Response:
    RESPONSE: dict = {
        "ok": False,
        "result": "lesson id is empty!"
    }
    return make_response(jsonify(RESPONSE), 400)


@api.route("/lesson/")
def redirect_root_lesson() -> redirect:
    return redirect(url_for("api.root_lesson"))


@api.route("/lesson/<int:lid>")
def search_lesson(lid) -> Response:
    RESPONSE: dict = dict()
    lesson: Lesson = Lesson.query.filter_by(id=lid).first()

    if not lesson:
        RESPONSE["ok"]: bool = False
        RESPONSE["result"]: str = "ID not found!"
        return make_response(jsonify(RESPONSE), 404)

    RESPONSE["ok"]: bool = True

    PREV: int = None if lesson.lid == 1 else Lesson.query \
        .filter_by(belong=lesson.belong) \
        .filter_by(lid=lesson.lid - 1).first().id

    NEXT: int = None \
        if lesson.lid == Lesson.query.filter_by(belong=lesson.belong).order_by(Lesson.lid).all()[-1].lid \
        else Lesson.query \
        .filter_by(belong=lesson.belong) \
        .filter_by(lid=lesson.lid + 1).first().id

    RESPONSE["lesson"]: dict = {
        "id": lesson.id,
        "uuid": lesson.uuid,
        "name": lesson.name,
        "prev": PREV,
        "next": NEXT,
        "description": lesson.desc,
        "url": lesson.url,
        "practices": [
            {
                "name": practice.name,
                "uuid": practice.uuid,
                "type": practice.type
            } for practice in lesson.practices.all()
        ]
    }
    return make_response(jsonify(RESPONSE))


@api.route("/lesson/<int:lid>/")
def redirect_lesson(lid) -> redirect:
    return redirect(url_for("api.search_lesson", lid=lid))
