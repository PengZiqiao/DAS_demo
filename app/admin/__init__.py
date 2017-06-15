from flask import url_for, redirect, request, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import db
from app.blueprints.auth.models import Role, User, role_required


class MyIndexView(AdminIndexView):
    @expose('/')
    @role_required('Admin')
    def index(self):
        return super(MyIndexView, self).index()


class MyModelView(ModelView):
    def is_accessible(self):
        # role_id 必须为1
        if current_user.is_authenticated and current_user.role_id == 1:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash('权限不足，请重新登陆：', 'danger')
        return redirect(url_for('auth.login', next=request.url))

    def __init__(self, mod, session, **kwargs):
        super(MyModelView, self).__init__(mod, session, **kwargs)


admin = Admin(index_view=MyIndexView(), template_mode='bootstrap3')
for mod in [Role, User]:
    admin.add_view(MyModelView(mod, db.session))
