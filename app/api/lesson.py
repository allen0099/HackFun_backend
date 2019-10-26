from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Lesson


@api.route("/lesson/<string:uuid>")
def root_lesson(uuid):
    q = Lesson.query.filter_by(uuid=uuid).first()
    return jsonify({
        "ok": True,
        "result": {
            "lesson": q.to_dict()
        }
    })


@api.route("/lesson/<string:uuid>/")
def redirect_lesson(uuid):
    return redirect(url_for("api.root_lesson", uuid=uuid))
