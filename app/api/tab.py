from flask import jsonify, make_response, Response, redirect, url_for

from app.api import api
from app.models import Tab


@api.route("/tab")
def root_tab() -> Response:
    tabs: list = Tab.query.all()
    RESPONSE: dict = dict()

    if not tabs:
        RESPONSE['result']: str = "No tabs found"
        return make_response(jsonify(RESPONSE), 404)

    RESPONSE["ok"]: bool = True
    RESPONSE["result"]: dict = {
        tab.name: [
            {
                "id": course.id,
                "name": course.name,
                "description": course.name
            } for course in tab.course.all()
        ] for tab in tabs
    }
    return make_response(jsonify(RESPONSE))


@api.route("/tab/")
def redirect_tab() -> redirect:
    return redirect(url_for("api.root_tab"))
