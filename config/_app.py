from abc import ABC
from os import environ
from flask import Flask, render_template
from flask_socketio import SocketIO


class Config(ABC):
    SECRET_KEY = environ.get('SECRET_KEY')


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    socketio = SocketIO(app)

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(409)
    @app.errorhandler(500)
    def invalid_route(e):
        return render_template("error.html", title=e.name, description=e.description, code=e.code), e.code

    return app, socketio
