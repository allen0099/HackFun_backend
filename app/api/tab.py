from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Tab


@api.route("/tab")
def root_tab():
    tabs = Tab.query.all()
    RESPONSE = {"ok": None}

    if not tabs:
        RESPONSE['result'] = "No tabs found"
        return jsonify(RESPONSE), 404

    RESPONSE["ok"] = True
    RESPONSE["result"] = {
        cards.name: [
            {
                "name": course.name,
                "description": course.description
            } for course in cards.course.all()
        ] for cards in tabs
    }
    return jsonify(RESPONSE)


@api.route("/tab/")
def redirect_tab():
    return redirect(url_for("api.root_tab"))
