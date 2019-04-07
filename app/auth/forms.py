from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    submit = SubmitField(label='提交')


class RegisterForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired(),
                                                    Length(1, 64),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                           '用户名必须由字母、数字、下划线或者 . 组成')])
    password = PasswordField(label='密码', validators=[DataRequired(),
                                                     EqualTo('password2', message='密码必须保持一致！')])
    password2 = PasswordField(label='确认密码', validators=[DataRequired()])
    email = StringField(label="邮箱", validators=[DataRequired(),
                                                Length(1, 64),
                                                Email()])
    submit = SubmitField(label='注册')


