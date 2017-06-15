from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    name = StringField('用户名', [DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', [DataRequired(message='密码不能为空')])
    submit = SubmitField('登陆')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', [DataRequired(message='旧密码不能为空')])
    password = PasswordField('新密码', [DataRequired(message='新密码不能为空'),
                                     EqualTo('confirm', message='两次密码输入不一致')])
    confirm = PasswordField('确认新密码')
    submit = SubmitField('修改')
