from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required,current_user

from . import bp
from .models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    from .forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('用户名或密码错误，请重新输入：', 'danger')
    return render_template('auth/login.html', **locals())


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功，请重新登陆', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    from .forms import ChangePasswordForm
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=current_user.name).first()
        if user.verify_password(form.old_password.data):
            user.change_password(form.password.data)
            flash('密码修改成功', 'success')
            form.old_password.data = ""
        else:
            flash('旧密码错误', 'danger')
            form.old_password.data = ""

    return render_template('auth/change_password.html', **locals())
