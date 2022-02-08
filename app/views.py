import os
from app import flask_app, db
from database.models import AppUser, Post, Photo, PersonalInfo, Place
from flask import request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask import g


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@flask_app.route("/")
@flask_app.route("/index")
def index():
    post = Post.query.get(1)
    post.add_comment_and_rate(1, "elegancko i fajniutko, pozdrawiam", 1)
    post.add_comment_and_rate(2, "bylo pite, fajna sprawa", 0)
    post.add_comment_and_rate(3, "grzecznie i z kultura", 1)
    return jsonify({"result": True})


@flask_app.route("/login", methods=["POST"], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return jsonify({"result": False})
    username = request.json["username"]
    password = request.json["password"]

    user = AppUser.query.filter_by(login=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"result": False})
    else:
        login_user(user)
        return jsonify({"result": True})


@flask_app.route("/register", methods=["POST"], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return jsonify({"result": False})

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    password1 = request.json["password1"]
    name = request.json.get("name", "Krystian")
    surname = request.json.get("surname", "Piotrowski")
    city = request.json.get("city", "Skierniewice")
    country_id = request.json.get("country", 1)
    sex_id = request.json.get("sex_id", 1)
    res_log = AppUser.validate_login(username)
    res_emil = AppUser.validate_email(email)
    if res_emil and res_log and password1 == password:
        try:
            personal_info = PersonalInfo(
                city=city,
                country_id=country_id,
                name=name,
                surname=surname,
                sex_id=sex_id,
            )
            db.session.add(personal_info)
            db.session.commit()
            user = AppUser(
                login=username, email=email, personal_info_id=personal_info.id
            )
            user.set_password(password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return jsonify({"result": True})
        except:
            db.session.rollback()
            return jsonify({"result": False})
    else:
        return jsonify({"result": False})


@flask_app.route("/logout")
def logout():
    logout_user()
    return jsonify({"result": False})


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


@flask_app.route("/user/<user_id>/add_post", methods=["POST"])
def result():
    post = request.json
    if post:
        result = current_user.add_post(
            text=post["text"], photo_path=post["photo_path"], visit_id=post["visit_id"]
        )
        return jsonify({"result": result})
    return "No player information is given"


@flask_app.route("/main", methods=["GET"])
def main():
    usr = AppUser.query.get(1)
    posts = usr.followed_posts()
    # posts = current_user.followed_posts() this will work after proper logging
    first_post = posts[0]
    comments = first_post.show_all_post_comments()
    visit = first_post.get_visit()
    return jsonify(
        {"post text": posts[0].text, "comment": comments[0].text, "visit": visit.name}
    )


def serializer(posts):
    return {
        "post_desc": posts[0],
        "username": posts[1],
        "id": posts[2],
        "avatar_path": posts[3],
        "photo_path": posts[4],
        "place": posts[5],
        "start_date": posts[6],
        "end_date": posts[7],
        "visit_name": posts[8],
        "comments": posts[9],
    }


@flask_app.route("/main_page", methods=["GET"])
def main_page():
    posts = Post.get_all_posts()
    serialized_posts = []
    for post in posts:
        user = AppUser.query.get(post.creator_id)
        avatar_path_rel = user.get_profile_photo()
        avatar_path = os.path.join(base_path, avatar_path_rel)
        photo_path_rel = Photo.query.filter_by(post_id=post.id).one()
        photo_path = os.path.join(base_path, photo_path_rel.photo_path)
        visit = post.get_visit()
        comments = post.show_all_post_comments()
        post_comments = []
        for comment in comments:
            creator = AppUser.query.get(comment.creator_id)
            post_comments.append({"username": creator.login, "comment": comment.text})
        place = Place.query.get(visit.place_id)
        serialized_posts.append(
            (
                post.text,
                user.login,
                post.id,
                avatar_path,
                photo_path,
                place.name,
                visit.start_date,
                visit.end_date,
                visit.name,
                post_comments
            )
        )
    return jsonify([*map(serializer, serialized_posts)])


@flask_app.route("/is_logged", methods=["GET"])
def is_logged():
    if current_user.is_authenticated:
        return jsonify({"result": True, "username": current_user.login})
    else:
        return jsonify({"result": False, "username": ""})


@flask_app.route("/get_post_id", methods=["POST"], strict_slashes=False)
def get_post_id():
    g.post_id = request.json['post_id']
    return jsonify({'result': True})


@flask_app.route("/post_site", methods=["GET"])
def post_site():
    post_id = g.post_id
    print(post_id)
    post = Post.query.get(post_id)
    print(post)
    return jsonify({'result': True})
