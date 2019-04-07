from flask import render_template, flash, redirect, url_for
from .forms import LoginForm, RegisterForm
from . import auth
from .. import db
from ..models import User
from flask_login import login_user, logout_user, current_user


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.hello_world'))
    return render_template('login.html', form=form, title='登录')


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(name=form.username.data,
                    password=form.password.data,
                    email=form.email.data,)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='注册', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

