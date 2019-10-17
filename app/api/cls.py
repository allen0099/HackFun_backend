from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Course, Class


@api.route("/class")
def root_class():
    return jsonify({
        "ok": False,
        "result": "Should pass course to get classes"
    }), 404


@api.route("/class/")
def redirect_root_class():
    return redirect(url_for("api.root_class"))


@api.route('/class/<string:course>', methods=['GET'])
def get_class(course):
    q = Course.query.filter_by(name=course).first()
    if q is None:
        return jsonify({
            "ok": False,
            "result": "No that course"
        }), 404
    return jsonify({
        "ok": True,
        "result": {
            "classes": [Class.to_dict(c) for c in q.classes.all()]
        }
    })


@api.route("/class/<string:course>/")
def redirect_class(course):
    return redirect(url_for("api.get_class", course=course))
