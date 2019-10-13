from flask import request, jsonify, abort

from app.api import api
from app.models import Topic


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
