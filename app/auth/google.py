import configparser

import requests
from flask import jsonify
from flask import request, abort
from flask_login import current_user
from oauthlib.oauth2 import WebApplicationClient

from app.auth import auth

# parse the config and pass them as Google credentials
config: configparser = configparser.ConfigParser()
config.read("credentials/google.ini")
google: dict = config['Google']

GOOGLE_CLIENT_ID: str = google['ID']
GOOGLE_CLIENT_SECRET: str = google['Secret']
GOOGLE_DISCOVERY_URL: str = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    try:
        r = requests.get(GOOGLE_DISCOVERY_URL)
    except requests.exceptions.ConnectionError:
        return abort(500, "No internet connection")
    if r.status_code == 200:
        return r.json()
    else:
        return abort(500, "Can't connect to Google now")


@auth.route("/google")  # /auth/google
def _login() -> jsonify:
    if not current_user.is_authenticated:
        # Find out what URL to hit for Google login
        google_provider_cfg: dict = get_google_provider_cfg()
        authorization_endpoint: str = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri: str = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.host_url + "callback/google",
            scope=["openid", "email", "profile"],
        )
        RESPONSE: dict = {
            "loggedIn": False,
            "uri": request_uri
        }
        return jsonify(RESPONSE)
    else:
        # User not login
        RESPONSE: dict = {
            "loggedIn": True
        }
        return jsonify(RESPONSE)
