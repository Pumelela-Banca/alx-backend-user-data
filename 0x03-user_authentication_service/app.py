#!/usr/bin/env python3
"""
Basic flask app
"""
import flask
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def start() -> str:
    """
    returns message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def give_passwrd() -> str:
    """
    gets password and email
    """
    email_user = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email_user, password)
        return jsonify(
            {"email": f"<{email_user}>", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    Creates a session
    """
    email_user = request.form.get("email")
    password = request.form.get("password")
    status = AUTH.valid_login(email=email_user, password=password)
    if not status:
        abort(401)
    session_id = AUTH.create_session(email=email_user)
    if session_id:
        resp = jsonify({"email": f"<{email_user}>", "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
