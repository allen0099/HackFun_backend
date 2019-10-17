from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Topic


@api.route("/topic")
def root_topic():
    return jsonify({
        "ok": False,
        "result": "Should pass topic's uuid"
    }), 404


@api.route("/topic/")
def redirect_topic():
    return redirect(url_for("api.root_topic"))


@api.route("/topic/<string:topic>")
def get_topic(topic):
    q = Topic.query.filter_by(uuid=topic).first()
    if q is None:
        return jsonify({
            "ok": False,
            "result": "Topic not found"
        }), 404
    return jsonify({
        "ok": True,
        "result": Topic.to_dict(q)
    })


@api.route("/topic/<string:topic>/")
def redirect_get_topic(topic):
    return redirect(url_for("api.get_topic", topic=topic))
