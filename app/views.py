import os
from app import flask_app
from database.models import AppUser, Post, Photo
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@flask_app.route("/")
@flask_app.route("/index")
def index():
    return "Hello World"


@flask_app.route("/login", methods=["POST"], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return jsonify({'result': False})
    username = request.json['username']
    password = request.json['body']

    user = AppUser.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'result': False})
    else:
        login_user(user)
        return jsonify({'result': True})


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


def serializer(posts):
    return {
        'post_desc': posts[0],
        'username': posts[1],
        'id': posts[2],
        'avatar_path': posts[3],
        'photo_path': posts[4]
    }


@flask_app.route("/main_page", methods=['GET'])
def main_page():
    posts = Post.get_all_posts()
    serialized_posts = []
    for post in posts:
        user = AppUser.query.get(post.creator_id)
        avatar_path_rel = user.get_profile_photo()
        avatar_path = os.path.join(base_path, avatar_path_rel)
        photo_path_rel = Photo.query.filter_by(post_id=post.id).one()
        photo_path = os.path.join(base_path, photo_path_rel.photo_path)
        serialized_posts.append((post.text, user.login, post.id, avatar_path, photo_path))
    return jsonify([*map(serializer, serialized_posts)])
