from functools import wraps

from flask import current_app, flash
from flask_login import UserMixin, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relation('User', backref='role')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def role_required(role_name):
    def wrap(func):
        @login_required
        def decorated_view(*args, **kwargs):
            role = Role.query.filter_by(name=role_name).first()
            if not current_user.role == role:
                flash('权限不足，请重新登陆：', 'danger')
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view

    return wrap
