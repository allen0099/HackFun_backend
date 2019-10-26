from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Tab


@api.route("/tab")
def root_tab():
    t = Tab.query.all()
    if not t:
        return jsonify({
            "ok": False,
            "result": "No tab found"
        }), 404
    return jsonify({
        "ok": True,
        "result": {
            "tabs": [Tab.get_name(c) for c in t]
        }
    })


@api.route("/tab/")
def redirect_tab():
    return redirect(url_for("api.root_tab"))
