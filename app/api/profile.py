from typing import List

from flask import Response, session, make_response, jsonify
from flask_login import login_required

from app.api import api
from app.models import Lesson, Practice, Complete, Course


@api.route("/profile")
@login_required
def root_profile() -> Response:
    uid: str = session.get("_user_id") or session.get("user_id")
    response: dict = {
        "ok": True,
        "uid": uid
    }

    response["personal"]: dict = {
        "lesson": None,
        "time": None,
        "latest": []
    }
    courses: List[Course] = Course.query.all()

    response["progress"]: dict = [
        {
            "course": course.name,
            "practices": {
                "complete": len(_get_complete_practices(uid, course)),
                "total": len(_get_all_practices(course))
            }
        } for course in courses
    ]

    return make_response(jsonify(response))


def _get_complete_practices(uid: str, course: Course) -> List[str]:
    complete: List[Complete] = Complete.query.filter_by(user_id=uid).all()
    uuid_all: List[str] = _get_all_practices(course)

    all_completed_uuid: List[str] = []
    for _ in complete:
        all_completed_uuid.append(_.practice_uuid)

    completed_uuid: List[str] = []
    for _ in all_completed_uuid:
        if _ in uuid_all:
            completed_uuid.append(_)

    return completed_uuid


def _get_all_practices(course: Course) -> List[str]:
    lessons: List[Lesson] = course.lessons.all()

    uuid_list: List[str] = []
    for lesson in lessons:
        practices: List[Practice] = lesson.practices.all()
        for practice in practices:
            uuid_list.append(practice.uuid)

    return uuid_list
