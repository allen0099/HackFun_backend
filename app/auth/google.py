from flask import request, jsonify
from flask_login import current_user

from app.auth import auth
from app.auth.callback import client, get_google_provider_cfg


@auth.route("/google")  # /auth/google
def _login():
    if not current_user.is_authenticated:
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.host_url + "callback/google",
            scope=["openid", "email", "profile"],
        )
        RESPONSE = {
            "logged-in": False,
            "uri": request_uri
        }
        return jsonify(RESPONSE)
    else:
        # User not login
        RESPONSE = {
            "logged-in": True
        }
        return jsonify(RESPONSE)
