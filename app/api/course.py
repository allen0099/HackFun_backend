from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Course


@api.route("/course/<string:name>")
def root_course(name) -> jsonify:
    RESPONSE: dict = {"ok": True}
    course: Course = Course.query.filter_by(name=name).first()

    if not course:
        RESPONSE["ok"]: bool = False
        RESPONSE["result"]: str = "Course not found"
        return jsonify(RESPONSE), 404

    RESPONSE["course"]: dict = {
        "name": course.name,
        "description": course.description,
        "lessons": [
            {
                "name": lesson.name,
                "description": lesson.description,
                "uuid": lesson.uuid,
                "url": lesson.url
            } for lesson in course.lessons.all()
        ],
        "overview": None
    }
    return jsonify(RESPONSE)


@api.route("/course/<string:name>/")
def redirect_course(name) -> redirect:
    return redirect(url_for("api.root_course", name=name))
