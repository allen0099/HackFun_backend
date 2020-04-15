from flask import jsonify, make_response, Response, redirect, url_for

from app.api import api
from app.models import Course


@api.route("/course")
def root_course() -> Response:
    RESPONSE: dict = {
        "ok": False,
        "result": "course id is empty!"
    }
    return make_response(jsonify(RESPONSE), 400)


@api.route("/course/")
def redirect_root_course() -> redirect:
    return redirect(url_for("api.root_course"))


@api.route("/course/<int:cid>")
def search_course(cid: int) -> Response:
    RESPONSE: dict = dict()
    course: Course = Course.query.filter_by(id=cid).first()

    if not course:
        RESPONSE["ok"]: bool = False
        RESPONSE["result"]: str = "ID not found!"
        return make_response(jsonify(RESPONSE), 404)

    RESPONSE["ok"]: bool = True
    RESPONSE["course"]: dict = {
        "id": course.id,
        "name": course.name,
        "description": course.desc,
        "prepareKnowledge": [
            {
                "description": knowledge.desc,
                "url": knowledge.url
            } for knowledge in course.knowledge.all()
        ],
        "lessons": [
            {
                "id": lesson.id,
                "name": lesson.name,
                "description": lesson.desc,
                "vid_url": lesson.vid_url
            } for lesson in course.lessons.all()
        ]
    }
    return make_response(jsonify(RESPONSE))


@api.route("/course/<int:cid>/")
def redirect_course(cid) -> redirect:
    return redirect(url_for("api.search_course", cid=cid))
