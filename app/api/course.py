from flask import jsonify, request, abort

from app.api import api
from app.models import Course, Class


@api.route('/course')
def root_course():
    return jsonify({
        "ok": True,
        "result": {
            "course": Course.get()
        }
    })


@api.route("/course", methods=['POST'])
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
