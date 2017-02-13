from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import logging
import src.models as models
import src.access as access
from src.stats_monitor import execute_command
import random
import string
from src.config_parser import ConfigParser

# set the logging mechanism
logging.basicConfig(filename="/var/log/event_log",
                    level=logging.DEBUG)


@app.route("/index", methods=['GET'])
def index():
    # redirect to login page
    # TODO: Insert sessions
    return render_template('login.html')


@app.route("/logged_in", methods=['GET'])
def logged_in():
    # redirect to login page
    # TODO: Insert sessions
    return render_template('index.html')


@app.route("/register", methods=['GET'])
def register():
    # redirect to register page
    return render_template('register.html')


@app.route("/admin", methods=['GET'])
def admin_page():
    # redirect to login page
    # TODO: Insert sessions
    return render_template('admin.html')


@app.route("/create_token", methods=['POST'])
def create_token():
    # generate new unique token
    token = models.Token.create_token()
    return jsonify({'token': token.token_id})


@app.route("/check_for_user", methods=['POST'])
def check_for_user():
    # redirect to login page
    # TODO: Insert sessions
    # TODO validate input
    access.register_new_user(request.form['username'],
                             request.form['hash'],
                             request.form['token'])
    result = {'authorized': False}
    return str(result['authorized'])


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route("/start_kodi")
def start_kodi():
    logging.info("Kodi started successfully!")
    return "All OK"


def read_and_format_log():
    with open("/var/log/event_log") as f:
        return f.read().replace('\n', '<br>')


@app.route("/retrieve_log")
def retrieve_log():
    return read_and_format_log()


@app.route("/start_gogs")
def start_gogs():
    result = execute_command(["/home/raspi/Downloads/gogs/gogs", "web"])

if __name__ == '__main__':
    app.run(port=5001, debug=True)
