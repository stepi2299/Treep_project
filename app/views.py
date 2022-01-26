from app import flask_app
from database.models import AppUser
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm



@flask_app.route('/')
@flask_app.route('/index')
def index():
    return "Hello World"


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)  #  not template but json


@flask_app.route('/logout')
def logout():
    login_user()
    return redirect(url_for('index'))


@flask_app.route("/user/<login>")
@login_required
def user(login):
    return jsonify("here will be json")


# TODO think how to do it with 3 forms and react
@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = AppUser(login=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)