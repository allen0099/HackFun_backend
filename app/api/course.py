from flask import jsonify, request, abort
from flask_login import login_required

from app.api import api
from app.models import Course, Class, Topic


@api.route('/course')
def course_root():
    """
    Show all course in json format
    :return all course list
    """
    return jsonify({
        "ok": True,
        "result": {
            "course": Course.get()
        }
    })


@api.route("/course", methods=['POST'])
@login_required
def post_course():
    """
    Add a new course to the database
    """
    content = request.json
    name = content.get("name")
    info = content.get("info")

    if name is None or info is None:
        return jsonify({
            "ok": False,
            "result": "name or info not supply"
        }), 400

    if name == "":
        return jsonify({
            "ok": False,
            "result": "name empty"
        }), 400

    check_query = Course.get(name)  # return list object
    if check_query is not None:  # duplicated
        return jsonify({
            "ok": False,
            "result": "Course duplicate"
        }), 400

    Course.add(name, info)
    return jsonify({
        "ok": True,
        "result": Course.get(name)
    })


@api.route('/course/<string:course>', methods=['GET'])
def get_course(course):
    """
    Search the course in the database
    :return all class in the course
    """
    find = Class.get(course)

    if find is None:
        return abort(404)

    return jsonify({
        "ok": True,
        "result": {
            "course": Course.get(course),
            "classes": find
        }
    })


@api.route('/topic', methods=['GET'])
def root_topic():
    tid = request.args.get("tid")
    course = request.args.get("course")

    if tid is not None and course is not None:
        return jsonify({
            "ok": False,
            "result": "can not pass both arguments in one query"
        }), 400

    if tid is not None:
        search = Topic.get(tid=tid)
        if search is None:
            return abort(404)
        return jsonify({
            "ok": True,
            "result": search
        })

    if course is not None:
        search = Topic.get(course=course)
        if search is None:
            return abort(404)
        return jsonify({
            "ok": True,
            "result": search
        })

    return jsonify({
        "ok": True,
        "result": Topic.get()
    })
