from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Course


@api.route("/course/<string:name>")
def root_course(name):
    q = Course.query.filter_by(belong=name).all()
    return jsonify({
        "ok": True,
        "result": {
            "course": [Course.to_dict(c) for c in q]
        }
    })


@api.route("/course/<string:name>/")
def redirect_course(name):
    return redirect(url_for("api.root_course", name=name))
