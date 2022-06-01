import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_sock import Sock


db = SQLAlchemy()
login_manager = LoginManager()
sock = Sock()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for folder in os.listdir(app.root_path + '/backend'):
        if os.path.isdir(app.root_path + '/backend/' + folder) and not folder.startswith('_'):
            module = import_module('apps.backend.' + folder + '.routes')
            app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def page_not_found(e):
    return render_template('error_pages/page-404.html'), 404


def forbidden(e):
    return render_template('error_pages/page-403.html'), 403


def internal_server_error(e):
    return render_template('error_pages/page-500.html'), 500


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internal_server_error)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    sock.init_app(app)

    return app
