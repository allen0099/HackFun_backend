from flask import jsonify, redirect, url_for

from app.api import api
from app.models import Tab


@api.route("/tab")
def root_tab() -> jsonify:
    tabs: list = Tab.query.all()
    RESPONSE: dict = {"ok": None}

    if not tabs:
        RESPONSE['result']: str = "No tabs found"
        return jsonify(RESPONSE), 404

    RESPONSE["ok"]: bool = True
    RESPONSE["result"]: dict = {
        cards.name: [
            {
                "name": course.name,
                "description": course.description
            } for course in cards.course.all()
        ] for cards in tabs
    }
    return jsonify(RESPONSE)


@api.route("/tab/")
def redirect_tab() -> redirect:
    return redirect(url_for("api.root_tab"))
