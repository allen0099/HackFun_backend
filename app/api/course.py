from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Course


@api.route("/course")
def root_course():
    course = Course.query.all()
    if not course:
        return jsonify({
            "ok": False,
            "result": "No course found"
        }), 404
    return jsonify({
        "ok": True,
        "result": {
            "course": [Course.to_dict(c) for c in course]
        }
    })


@api.route("/course/")
def redirect_root():
    return redirect(url_for("api.root_course"))
