import os
from app import flask_app, db
from database.models import AppUser, Post, Photo, PersonalInfo, Place, PlaceAdmin, Attraction, Hotel, ProfilePhoto
from flask import request, jsonify, session, send_file, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

global post_id


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
        return jsonify({"result": False,
                        "exp": 0,
                        "upper_bound": 0,
                        "star1": False,
                        "star2": False,
                        "star3": False
                        })
    else:
        login_user(user)
        exp_level, high_bound = current_user.get_exp_level()
        return jsonify({"result": True,
                        "exp": current_user.experience,
                        "upper_bound": high_bound,
                        "star1": exp_level[0],
                        "star2": exp_level[1],
                        "star3": exp_level[2]
                        })


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


@flask_app.route("/user", methods=["POST"], strict_slashes=False)
def user():
    username = request.json["username"]
    user = AppUser.query.filter_by(login=username).one()
    exp_level, high_boundry = user.get_exp_level()
    avatar_path_rel = user.get_profile_photo()
    abc_path = "http://127.0.0.1:8000/"
    avatar_path = os.path.join(abc_path, avatar_path_rel)
    info = user.get_personal_info()
    country = info.get_user_country()
    try:
        if user.login == current_user.login:
            ownership = True
        else:
            ownership = False
    except:
        ownership = False
    user_visits = user.all_user_visits()
    user_posts = user.show_user_posts()
    user_places = user.visited_places()
    posts = []
    visits = []
    for post in user_posts:
        posts.append(post)
    for visit in user_visits:
        visits.append(visit)
    return jsonify(
        {
            "username": user.login,
            "post_count": user_posts.count(),
            "name": info.name,
            "surname": info.surname,
            "country": country.country,
            "exp": user.experience,
            "avatar_path": avatar_path,
            "star1": exp_level[0],
            "star2": exp_level[1],
            "star3": exp_level[2],
            "upper_bound": high_boundry,
            "is_you": ownership,
            "visits": "dontknow",
            "posts": "dontknow",
            "places": "usr_places",
        }
    )


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
        abc_path = "http://127.0.0.1:8000/"
        avatar_path = os.path.join(abc_path, avatar_path_rel)
        photo_path_rel = Photo.query.filter_by(post_id=post.id).one()
        photo_path = os.path.join(abc_path, photo_path_rel.photo_path)
        visit = post.get_visit()
        comments = post.show_all_post_comments()
        post_comments = []
        for comment in comments:
            creator = comment.get_creator()
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
                post_comments,
            )
        )
    return jsonify([*map(serializer, serialized_posts)])

@flask_app.route("/photo_post", methods=["POST"])
def photo():
    photo_path = request.json["photo_path"]
    print(send_file(photo_path))
    return send_file(photo_path)



@flask_app.route("/is_logged", methods=["GET"])
def is_logged():
    if current_user.is_authenticated:
        exp_level, high_bound = current_user.get_exp_level()
        abc_path = "http://127.0.0.1:8000/"
        user = current_user
        avatar_path_rel = user.get_profile_photo()
        avatar_path = os.path.join(abc_path, avatar_path_rel)
        return jsonify(
            {
                "result": True,
                "username": current_user.login,
                "exp": current_user.experience,
                "upper_bound": high_bound,
                "star1": exp_level[0],
                "star2": exp_level[1],
                "star3": exp_level[2],
                "avatar_path": avatar_path
            }
        )
    else:
        return jsonify(
            {
                "result": False,
                "username": "",
                "exp": 0,
                "upper_bound": 0,
                "star1": False,
                "star2": False,
                "star3": False
            }
        )


@flask_app.route("/post_site", methods=["POST"], strict_slashes=False)
def post_site():
    post_id = request.json["post_id"]
    post = Post.query.get(post_id)
    user = post.get_creator()
    photo = post.get_photo()
    visit = post.get_visit()
    place = visit.get_place()
    abc_path = "http://127.0.0.1:8000/"
    user = AppUser.query.get(post.creator_id)
    avatar_path_rel = user.get_profile_photo()
    avatar_path = os.path.join(abc_path, avatar_path_rel)
    comments = post.show_all_post_comments()
    post_comments = []
    abc_path = "http://127.0.0.1:8000/"
    photo_path = os.path.join(abc_path, photo.photo_path)
    try:
        if user.login == current_user.login:
            ownership = True
        else:
            ownership = False
    except:
        ownership = False
    for comment in comments:
        creator = comment.get_creator()
        post_comments.append({"username": creator.login, "comment": comment.text})
    post_objects = {
        "username": user.login,
        "text": post.text,
        "avatar_path": avatar_path,
        "photo_path": photo_path,
        "place_name": place.name,
        "visit_name": visit.name,
        "start_date": visit.start_date,
        "end_date": visit.end_date,
        "comments": post_comments,
        "your_post": ownership,
    }
    return jsonify(post_objects)


@flask_app.route("/add_post", methods=["POST"], strict_slashes=False)
def add_post():
    text = request.json["text"]
    photo_path_name = request.json.get("photo_path", None)
    photo_path = os.path.join("app", "static", "img", photo_path_name)
    visit_id = request.json.get("visit_id")
    result = current_user.add_post(text, photo_path, visit_id)
    if result:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})


@flask_app.route("/add_comment", methods=["POST"], strict_slashes=False)
def add_comment():
    post_id = request.json["post_id"]
    text = request.json["text"]
    note = request.json.get("note", 0)
    post = Post.query.get(post_id)
    result = post.add_comment_and_rate(current_user.id, text, int(note["name"]))
    if result:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})


@flask_app.route("/add_visit", methods=["POST"], strict_slashes=False)
def add_visit():
    place_id = request.json.get("place_id")
    hotel_id = request.json.get("hotel_id", None)
    transport_id = request.json.get("transport_id", None)
    attraction_id = request.json.get("attraction_id", None)
    name = request.json["name"]
    start_date = request.json["start_date"]
    end_date = request.json["end_date"]
    result = current_user.add_visit(
        place_id, hotel_id, transport_id, name, start_date, end_date, attraction_id
    )
    if result:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})


@flask_app.route("/add_place", methods=["POST"], strict_slashes=False)
def add_place():
    try:
        name = request.json["name"]
        country_id = request.json.get("country_id", 1)
        language = request.json.get("language", "pl")
        region = request.json.get("region", None)
        admin = PlaceAdmin.query.get(current_user.id)
        result = admin.add_place(name, country_id, language, region)
        if result:
            return jsonify({"result": True})
        else:
            return jsonify({"result": False})
    except:
        return jsonify({"result": False})


@flask_app.route("/add_hotel", methods=["POST"], strict_slashes=False)
def add_hotel():
    place_id = request.json["place_id"]
    name = request.json["name"]
    country_id = request.json["country_id"]
    city = request.json["city"]
    street = request.json["street"]
    nr_of_street = request.json["nr_of_street"]
    nr_apartment = request.json.get("nr_apartment", None)
    postcode = request.json.get("postcode", None)
    google_maps_link = request.json.get("google_maps_link", None)
    site_link = request.json.get("site_link", None)
    place = Place.query.get(place_id)
    result = place.add_hotel(
        name,
        country_id,
        city,
        street,
        nr_of_street,
        current_user.id,
        nr_apartment,
        postcode,
        google_maps_link,
        site_link,
    )
    if result:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})


@flask_app.route("/add_attraction", methods=["POST"], strict_slashes=False)
def add_attraction():
    place_id = request.json["place_id"]
    name = request.json["name"]
    description = request.json["description"]
    photo_path = request.json["photo_path"]
    google_maps = request.json.get("google_maps", None)
    site_link = request.json.get("site_link", None)
    place = Place.query.get(place_id)
    result = place.add_attraction(
        name, description, photo_path, current_user.id, google_maps, site_link,
    )
    if result:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})


@flask_app.route("/get_visits", methods=["POST"], strict_slashes=False)
def get_visits():
    username = request.json["username"]
    user = AppUser.query.filter_by(login=username).first()
    visits_list = []
    visits = user.all_user_visits()
    for visit in visits:
        visits_list.append({"id": visit.id,
                            "visit": visit.name})
    return jsonify(visits_list)


@flask_app.route("/get_places", methods=["GET"])
def get_places():
    places_list = []
    places = Place.get_all_places()
    for place in places:
        places_list.append({"id": place.id,
                            "name": place.name})
    return jsonify(places_list)


@flask_app.route("/get_attractions", methods=["GET"])
def get_attractions():
    attraction_list = []
    attractions = Attraction.get_all_attractions()
    for attraction in attractions:
        attraction_list.append({"id": attraction.id,
                                "name": attraction.name})
    return jsonify(attraction_list)


@flask_app.route("/get_hotels", methods=["GET"])
def get_hotels():
    hotels_list = []
    hotels = Hotel.get_all_hotels()
    for hotel in hotels:
        hotels_list.append({"id": hotel.id,
                            "name": hotel.name})
    return jsonify(hotels_list)


@flask_app.route("/edit_profile", methods=["POST"], strict_slashes=False)
def edit_profile():
    try:
        username = request.json["username"]
        avatar_name = request.json.get("photo_path", None)
        user = AppUser.query.filter_by(login=username).first()
        personal_info = PersonalInfo.query.get(user.personal_info_id)
        name = request.json.get("name", personal_info.name)
        if not name:
            name = personal_info.name
        surname = request.json.get("surname", personal_info.surname)
        if not surname:
            surname = personal_info.surname
        city = request.json.get("city", personal_info.city)
        country_id = request.json.get("country", personal_info.country_id)
        sex_id = request.json.get("sex_id", personal_info.sex_id)
        personal_info.edit_personal_info(name, surname, city, country_id, sex_id)
        db.session.add(personal_info)
        db.session.commit()
        print(avatar_name)
        if avatar_name:
            print(1)
            avatar_path = os.path.join("app", "static", "profile", avatar_name)
            print(avatar_path)
            profile_photo = ProfilePhoto(photo_path=avatar_path)
            print("dad")
            db.session.add(profile_photo)
            db.session.commit()
            print(user.profile_photo)
            user.add_profile_photo(profile_photo.id)
            print(user.profile_photo)
            db.session.add(user)
            db.session.commit()
            print(avatar_path)
        return jsonify({"result": True})
    except:
        db.session.rollback()
        return jsonify({"result": False})


@flask_app.route("/edit_post", methods=["POST"], strict_slashes=False)
def edit_post():
    try:
        post_id = request.json["post_id"]
        post = Post.query.get(post_id)
        text = request.json.get("text", post.text)
        visit_id = request.json.get("visit_id", post.visit_id)
        post.edit_post(text=text, visit_id=visit_id)
        db.session.add(post)
        db.session.commit()
        return jsonify({"result": True})
    except:
        db.session.rollback()
        return jsonify({"result": False})
