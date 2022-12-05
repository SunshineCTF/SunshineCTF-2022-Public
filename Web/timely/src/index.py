# from flask.ext.sqlalchemy import SQLAlchemy
import logging
import os
import random
from logging import FileHandler, Formatter

from flask import Flask, Response, make_response, render_template, request

app = Flask(__name__)
app.config.from_object("config")


@app.route("/")
def home():
    return render_template("pages/home.html")


@app.route("/robots.txt")
def robots():
    response = make_response("Disallow: /dev", 200)
    response.mimetype = "text/plain"
    return response


@app.route("/dev")
def dev():
    response = make_response("/hostname\n/users", 200)
    response.mimetype = "text/plain"
    return response


@app.route("/dev/hostname")
def hostname():
    response = make_response(os.uname(), 200)
    response.mimetype = "text/plain"
    return response


@app.route("/dev/users")
def users():
    response = make_response(
        "ahrifan111 (Disabled)\nanri (Active)\nadmin (Disabled)\ndevelop (Disabled)",
        200,
    )
    response.mimetype = "text/plain"
    return response


@app.route("/login", methods=["GET"])
def loginpage():
    return render_template("pages/login.html")


@app.route("/login", methods=["POST"])
def loginpost():
    d = request.get_json()
    username = d.get("username")
    phash = d.get("password")

    HASH = app.config.get("HASH")
    FLAG = app.config.get("FLAG")

    if not username or not phash:
        return "You forgot something...", 400

    if username != "anri":
        return "You're not a true fan :C", 401

    if len(phash) != len(HASH):
        return "Nope. Wrong.", 401

    resp = Response("Nope. Wrong.")

    i = 0
    variation = random.randrange(-20, 20)
    for user_c, secret_c in zip(str(phash), HASH):
        # print(user_c, secret_c)
        if user_c != secret_c:
            resp.headers["Debug-Lag-Fix"] = f"{i*100+variation}ns"
            return resp, 401
        else:
            i += 1

    return f"Congrats! {FLAG}", 200
    # return render_template("pages/login.html")


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

def create_app():
    return app
