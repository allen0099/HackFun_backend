from flask import jsonify, make_response, Response, redirect, url_for, session

from app.api import api
from app.models import Lesson, Choose, Docker, Practice, Visited, Complete, VidRecord


@api.route("/lesson")
def root_lesson() -> Response:
    response: dict = {
        "ok": False,
        "result": "lesson id is empty!"
    }
    return make_response(jsonify(response), 400)


@api.route("/lesson/")
def redirect_root_lesson() -> redirect:
    return redirect(url_for("api.root_lesson"))


@api.route("/lesson/<int:lid>")
def search_lesson(lid: int) -> Response:
    response: dict = dict()
    lesson: Lesson = Lesson.query.filter_by(id=lid).first()

    if not lesson:
        response["ok"]: bool = False
        response["result"]: str = "ID not found!"
        return make_response(jsonify(response), 404)

    uid: str = session.get("_user_id") or session.get("user_id")

    if uid is not None:
        Visited.add(uid, lid)

    response["ok"]: bool = True

    _prev: int = None \
        if lesson.order_id == 1 \
        else Lesson.query \
        .filter_by(course_id=lesson.course_id) \
        .filter_by(order_id=lesson.order_id - 1).first().id

    _next: int = None \
        if lesson.order_id == Lesson.query \
        .filter_by(course_id=lesson.course_id) \
        .order_by(Lesson.order_id).all()[-1].order_id \
        else Lesson.query \
        .filter_by(course_id=lesson.course_id) \
        .filter_by(order_id=lesson.order_id + 1).first().id

    record: VidRecord = None if uid is None else VidRecord.query.filter_by(lesson_id=lid).filter_by(user_id=uid).first()

    response["lesson"]: dict = {
        "id": lesson.id,
        "uuid": lesson.uuid,
        "name": lesson.name,
        "course": lesson.course.name,
        "prev": _prev,
        "next": _next,
        "index": lesson.order_id,
        "description": lesson.desc,
        "vid_url": lesson.vid_url,
        "vid_sec": 0 if uid or record is None else record.time,
        "vid_progress": 0 if uid or record is None else record.progress
    }

    practices: list = []
    for practice in lesson.practices.all():
        practices.append(
            get_practice(practice)
        )

    response["lesson"]["practices"]: list = practices
    return make_response(jsonify(response))


@api.route("/lesson/<int:lid>/")
def redirect_lesson(lid) -> redirect:
    return redirect(url_for("api.search_lesson", lid=lid))


def get_practice(practice: Practice) -> dict:
    choose = None
    docker = None
    if practice.choose.first():
        practice.type = "choose"
        _choose: Choose = practice.choose.first()
        if _choose is not None:
            choose = {
                "statement": _choose.statement,
                "options": [
                    {
                        "id": option.id,
                        "value": option.statement
                    } for option in _choose.option.all()
                ]
            }
    elif practice.docker.first():
        practice.type = "docker"
        _docker: Docker = practice.docker.first()
        if _docker is not None:
            docker = {
                "description": _docker.desc,
                "url": _docker.url,
                "port": _docker.port,
                "file_hash": _docker.file_hash
            }

    uid: str = session.get("_user_id") or session.get("user_id")
    solved: bool = False
    if uid is not None:
        solved = Complete.is_solved(uid, practice.uuid)

    return {
        "id": practice.id,
        "uuid": practice.uuid,
        "name": practice.name,
        "hints": [
            hint.desc for hint in practice.hint.all()
        ],
        "type": practice.type,
        "choose": choose,
        "docker": docker,
        "solved": solved
    }
