from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import find_modules, import_string

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请输入您的用户名和密码：'
login_manager.login_message_category = 'mute'


def create_app():
    from app.admin import admin
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    for name in find_modules('app.blueprints', include_packages=True):
        mod = import_string(name)
        app.register_blueprint(mod.bp)
