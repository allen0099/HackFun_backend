import configparser
import json

import requests
from flask import request, abort, jsonify, redirect, url_for
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from oauthlib.oauth2 import WebApplicationClient

from app.authorization import authorized
from app.models import User

# parse the config and pass them as Google credentials
config = configparser.ConfigParser()
config.read("credentials.ini")
GOOGLE_CLIENT_ID = config['GoogleClient']['ID']
GOOGLE_CLIENT_SECRET = config['GoogleClient']['Secret']
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# flask login user model
login_manager = LoginManager()


@login_manager.user_loader
def load_user(uid):
    # return user, not str
    return User.get(uid)


def get_google_provider_cfg():
    try:
        r = requests.get(GOOGLE_DISCOVERY_URL)
    except requests.exceptions.ConnectionError:
        return abort(500, "No internet connection")
    if r.status_code == 200:
        return r.json()
    else:
        return abort(500, "Can't connect to Google now")


@authorized.route("/user")
@login_required
def _user():
    RESPONSE = {
        "ok": True,
        "result": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "pic": current_user.profile_pic
        }
    }
    return jsonify(RESPONSE)


@authorized.route("/login")
def _login():
    if not current_user.is_authenticated:
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.host_url + "login/callback",
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


@authorized.route("/login/callback")
def _callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    if not code:
        return abort(400)

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    if token_response.json().get("access_token", None) is None:
        return abort(400)
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        # update user's data each time user login
        if User.get(unique_id) is None:
            User.add(unique_id, users_name, users_email, picture)
        else:
            User.update(unique_id, users_name, users_email, picture)

        # Login user
        user = User(unique_id, users_name, users_email, picture)
        login_user(user)

        return redirect(url_for("login._user"))
    else:
        return abort(400, "User email not available or not verified by Google.")


@authorized.route("/logout")
@login_required
def logout():
    logout_user()
    RESPONSE = {"ok": True,
                "result": "logout success!"}
    return jsonify(RESPONSE)
