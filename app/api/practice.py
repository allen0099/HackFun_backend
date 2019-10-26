from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Practice


@api.route("/practice/<string:uuid>")
def root_practice(uuid):
    q = Practice.query.filter_by(uuid=uuid).first()
    return jsonify({
        "ok": True,
        "result": {
            "practice": q.to_dict()
        }
    })


@api.route("/practice/<string:uuid>/")
def redirect_practice(uuid):
    return redirect(url_for("api.root_practice", uuid=uuid))
