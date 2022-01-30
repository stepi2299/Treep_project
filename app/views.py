from app import flask_app
from database.models import AppUser
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm


@flask_app.route("/")
@flask_app.route("/index")
def index():
    return "Hello World"


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(url_for("index"))
    return render_template(
        "login.html", title="Sign In", form=form
    )  #  not template but json


@flask_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@flask_app.route("/user/<user_id>", methods=["GET"])
def user(user_id):
    usr = AppUser.query.get(user_id)
    usr_visits = usr.all_user_visits()
    usr_posts = usr.show_user_posts()
    usr_places = usr.visited_places()
    posts = []
    visits = []
    for post in usr_posts:
        posts.append(post)
    for visit in usr_visits:
        visits.append(visit)
    return jsonify(
        {
            "user": usr.login,
            "visits": visits[0].name,
            "posts": posts[0].text,
            "places": usr_places,
        }
    )


@flask_app.route('/user/<user_id>/add_post', methods=['POST'])
def result():
    post = request.json
    if post:
        result = current_user.add_post(text=post['text'], photo_path=post['photo_path'], visit_id=post['visit_id'])
        return jsonify({"result": result})
    return "No player information is given"


@flask_app.route("/main", methods=['GET'])
def main():
    usr = AppUser.query.get(1)
    posts = usr.followed_posts()
    #posts = current_user.followed_posts() this will work after proper logging
    first_post = posts[0]
    comments = first_post.show_all_post_comments()
    visit = first_post.get_visit()
    return jsonify({'post text': posts[0].text,
                    'comment': comments[0].text,
                    'visit': visit.name})
