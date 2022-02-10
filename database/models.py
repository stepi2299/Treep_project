from app import db, login
from core.reports import ReportField, Report
from core.user_interaction import UserInteraction
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import datetime
import pytz


@login.user_loader
def load_user(id):
    return AppUser.query.get(int(id))


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("AppUser.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("AppUser.id")),
)

user_interests = db.Table(
    "user_interests",
    db.Column("user_id", db.Integer, db.ForeignKey("AppUser.id")),
    db.Column("interest_id", db.Integer, db.ForeignKey("TypeOfInterests.id")),
)

attraction_interests = db.Table(
    "attraction_interests",
    db.Column("attraction_id", db.Integer, db.ForeignKey("Attraction.id")),
    db.Column("interest_id", db.Integer, db.ForeignKey("TypeOfInterests.id")),
)

visit_attractions = db.Table(
    "visit_attractions",
    db.Column("visit_id", db.Integer, db.ForeignKey("Visit.id")),
    db.Column("attraction_id", db.Integer, db.ForeignKey("Attraction.id")),
)


class TypeOfInterests(db.Model):
    __tablename__ = "TypeOfInterests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class AppUser(db.Model, ReportField, UserMixin):
    __tablename__ = "AppUser"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    experience = db.Column(db.Integer, default=0)
    experience_level_id = db.Column(
        db.Integer, db.ForeignKey("ExperienceLevel.id"), default=1
    )
    personal_info_id = db.Column(
        db.Integer, db.ForeignKey("PersonalInfo.id"), nullable=False, unique=True
    )
    password_hash = db.Column(db.String(128))
    followed = db.relationship(
        "AppUser",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    interest = db.relationship(
        "TypeOfInterests",
        secondary=user_interests,
        primaryjoin=(user_interests.c.user_id == id),
        secondaryjoin=(user_interests.c.interest_id == TypeOfInterests.id),
        backref=db.backref("interest", lazy="dynamic"),
        lazy="dynamic",
    )
    profile_photo = db.Column(db.Integer, db.ForeignKey("ProfilePhoto.id"), default=1)

    def __init__(self, login, email, personal_info_id, experience=0):
        self.login = login
        self.email = email
        self.experience = experience
        self.personal_info_id = personal_info_id
        self.__update_level_experience()

    def __repr__(self):
        return f"user: {self.login}"

    def get_profile_photo(self):
        photo = ProfilePhoto.query.get(self.profile_photo)
        return photo.photo_path

    def get_personal_info(self):
        return PersonalInfo.query.get(self.personal_info_id)

    def get_exp_level(self):
        if self.experience_level_id == 1:
            return {"1_star": True,
                    "2_star": False,
                    "3_star": False
                    }, 100
        elif self.experience_level_id == 2:
            return {"1_star": True,
                    "2_star": True,
                    "3_star": False
                    }, 200
        else:
            return {"1_star": True,
                    "2_star": True,
                    "3_star": True
                    }, "max"

    @staticmethod
    def validate_login(login):
        user = AppUser.query.filter_by(login=login).first()
        if user is not None:
            return False
        return True

    @staticmethod
    def validate_email(email):
        user = AppUser.query.filter_by(email=email).first()
        if user is not None:
            return False
        return True

    def create_report(self, reporter_id, reason):
        try:
            report = UserReport(
                reporter_id=reporter_id, reason=reason, reported_id=self.id
            )
            db.session.add(report)
            db.session.commit()
            return report
        except:
            db.session.rollback()
            return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_post(self, text, photo_path, visit_id=None):
        try:
            post = Post(text=text, creator_id=self.id, visit_id=visit_id)
            db.session.add(post)
            db.session.commit()
            photo = Photo(photo_path=photo_path, post_id=post.id)
            db.session.add(photo)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def hide_interaction(self, post_id, deletion_cause):
        try:
            post = Post.query.get(post_id)
            post.can_delete(self.experience_level_id)
            if post.can_delete:
                post.deleted = True
                post.deletion_cause = deletion_cause
                post.deletion_user = self.id
                db.session.add(post)
                db.session.commit()
                return True
            else:
                return False
        except:
            db.session.rollback()
            return False

    def add_experience(self, experience_diff):
        if self.experience >= experience_diff:
            self.experience += experience_diff
        else:
            self.experience = 0
        self.__update_level_experience()

    def __update_level_experience(self):
        if self.experience < 100:
            self.experience_level_id = 1
        elif 100 <= self.experience <= 200:
            self.experience_level_id = 2
        else:
            self.experience_level_id = 3

    def add_visit(self, place_id, hotel_id, transport_id, name, start_date, end_date):
        try:
            visit = Visit(
                place_id=place_id,
                hotel_id=hotel_id,
                transport_id=transport_id,
                user_id=self.id,
                name=name,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.add(visit)
            db.session.commit()
            return visit
        except:
            db.session.rollback()
            return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def add_interest(self, type_of_interest):
        if not self.already_interest(type_of_interest):
            self.interest.append(type_of_interest)

    def delete_interest(self, type_of_interest):
        if self.already_interest(type_of_interest):
            self.interest.delete(type_of_interest)

    def already_interest(self, type_of_interest):
        return (
            self.interest.filter(
                user_interests.c.interest_id == type_of_interest.id
            ).count()
            > 0
        )

    def show_user_posts(self):
        return (
            Post.query.filter_by(creator_id=self.id)
            .order_by(Post.creation_date.desc())
        )

    def followed_posts(self):
        # photos!!!
        followed = (
            Post.query.join(followers, (followers.c.followed_id == Post.creator_id))
            .filter(followers.c.follower_id == self.id)
            .order_by(Post.creation_date.desc())
        )
        own = self.show_user_posts()
        return followed.union(own).order_by(Post.creation_date.desc())

    def all_user_visits(self):
        visits = Visit.query.filter_by(user_id=self.id).order_by(Visit.end_date.desc())
        return visits

    def visited_places(self):
        # TODO implement query (with join from visit)
        return list()


class PersonalInfo(db.Model):
    __tablename__ = "PersonalInfo"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), index=True)
    country_id = db.Column(db.Integer, db.ForeignKey("Country.id"), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    sex_id = db.Column(db.Integer, db.ForeignKey("Sex.id"))
    surname = db.Column(db.String(80))

    def get_user_country(self):
        return Country.query.get(self.country_id)


class Moderator(AppUser, db.Model):
    __tablename__ = "Moderator"

    id = db.Column(db.Integer, db.ForeignKey("AppUser.id"), primary_key=True)

    def __init__(self, login, email, personal_info_id, experience=0):
        super().__init__(
            login=login,
            email=email,
            experience=experience,
            personal_info_id=personal_info_id,
        )

    @staticmethod
    def delete_interaction(model, interaction_id):
        try:
            interaction = model.query.get(interaction_id)
            db.session.delete(interaction)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def consider_report(self, report_id, settlement_id, model):
        try:
            report = model.query.get(report_id)
            report.settlement_id = settlement_id
            report.admin_id = self.id
            report.settlement_date = datetime.date.today()
            if settlement_id == 3:
                Moderator.delete_interaction(model, report.interaction_id)
            db.session.add(report)
            db.session.commit()
            return report
        except:
            db.session.rollback()
            return False

    @staticmethod
    def show_all_reports(model):
        try:
            reports = model.query.all()
            return reports
        except:
            return False

    @staticmethod
    def show_all_not_considered_reports(model):
        try:

            reports = model.query.filter_by(settlement_id=1)
            return reports
        except:
            return False




class UserAdmin(AppUser):
    __tablename__ = "UserAdmin"

    id = db.Column(db.Integer, db.ForeignKey("AppUser.id"), primary_key=True)

    def __init__(self, login, email, personal_info_id, experience=0):
        super().__init__(
            login=login,
            email=email,
            experience=experience,
            personal_info_id=personal_info_id,
        )


class PlaceAdmin(AppUser):
    __tablename__ = "PlaceAdmin"

    id = db.Column(db.Integer, db.ForeignKey("AppUser.id"), primary_key=True)

    def __init__(self, login, email, personal_info_id, experience=0):
        super().__init__(
            login=login,
            email=email,
            experience=experience,
            personal_info_id=personal_info_id,
        )

    def add_place(self, name):
        try:
            place = Place(name=name, admin_id=self.id)
            db.session.add(place)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete_place(place_id):
        try:
            place = Place.query.get(place_id)
            db.session.delete(place)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def consider_report(self, report_id, settlement_id):
        try:
            report = PlaceReport.query.get(report_id)
            report.settlement_id = settlement_id
            report.admin_id = self.id
            report.settlement_date = datetime.date.today()
            db.session.add(report)
            db.session.commit()
            return report
        except:
            db.session.rollback()
            return False

    @staticmethod
    def show_all_reports():
        try:
            reports = PlaceReport.query.all()
            return reports
        except:
            return False

    @staticmethod
    def show_all_not_considered_reports():
        try:
            reports = PlaceReport.query.filter_by(settlement_id=1)
            return reports
        except:
            return False


class Post(db.Model, UserInteraction):
    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("Visit.id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"), nullable=False)
    creation_date = db.Column(db.DateTime, index=True)
    text = db.Column(db.String(3000), nullable=False)
    note = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    deletion_cause = db.Column(db.String(100))
    deletion_user = db.Column(db.Integer, db.ForeignKey("AppUser.id"))

    def __init__(self, creator_id, text, visit_id, note=0):
        super().__init__(text=text)
        self.creator_id = creator_id
        self.visit_id = visit_id
        self.note = note
        self.can_delete = False

    def can_delete(self, viewer_exp_level_id):
        creator = AppUser.query.get(self.creator_id)
        if viewer_exp_level_id > creator.experience_level_id:
            self.can_delete = True
        else:
            self.can_delete = False

    def create_report(self, reporter_id, reason):
        try:
            report = PostReport(reporter_id=reporter_id, reason=reason, interaction_id=self.id)
            db.session.add(report)
            db.session.commit()
            return report
        except:
            db.session.rollback()
            return False

    def add_comment_and_rate(self, user_id, text, note):
        try:
            comment = Comment(creator_id=user_id, post_id=self.id, text=text, note=note)
            db.session.add(comment)
            db.session.commit()
            user = AppUser.query.get(self.creator_id)
            user.add_experience(note)
            return comment
        except:
            db.session.rollback()
            return False

    def show_all_post_comments(self):
        try:
            return (
                Comment.query.filter_by(post_id=self.id)
                .order_by(Comment.creation_date.desc())
                .all()
            )
        except:
            return False

    def get_visit(self):
        return Visit.query.filter_by(id=self.visit_id).one()

    @staticmethod
    def get_all_posts():
        return Post.query.order_by(Post.note.desc()).all()

    def get_creator(self):
        return AppUser.query.get(self.creator_id)

    def get_photo(self):
        return Photo.query.filter_by(post_id=self.id).first()



class Comment(db.Model, UserInteraction):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"))
    attraction_id = db.Column(db.Integer, db.ForeignKey("Attraction.id"))
    creation_date = db.Column(
        db.DateTime, default=datetime.datetime.now(pytz.utc), index=True
    )
    text = db.Column(db.String(200))
    given_note = db.Column(db.Integer)

    def __init__(self, text, note, creator_id, post_id=None, attraction_id=None):
        super().__init__(text=text)
        self.post_id = post_id
        self.attraction_id = attraction_id
        self.given_note = note
        self.creator_id = creator_id

    def create_report(self, reporter_id, reason):
        try:
            report = CommentReport(
                reporter_id=reporter_id, reason=reason, interaction_id=self.id
            )
            db.session.add(report)
            db.session.commit()
            return report
        except:
            db.session.rollback()
            return False

    def get_creator(self):
        return AppUser.query.get(self.creator_id)


class Place(db.Model, ReportField):
    __tablename__ = "Place"

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, index=True)
    name = db.Column(db.String(40), index=True, unique=True, nullable=False)
    geo_information_id = db.Column(
        db.Integer, db.ForeignKey("GeoInformation.id"), nullable=False
    )
    admin_id = db.Column(db.Integer, db.ForeignKey("PlaceAdmin.id"))
    attractions = db.relationship("Attraction", backref="main_place", lazy="dynamic")
    hotels = db.relationship("Hotel", backref="main_place", lazy="dynamic")
    communications = db.relationship("Transport", backref="main_place", lazy="dynamic")

    def __init__(self, admin_id, name, country_id, language, region):
        self.admin_id = admin_id
        self.name = name
        self.creation_date = datetime.date.today()
        self.__add_geo_information(country_id, language, region)
        self.average_weather = None  # TODO think how show the weather
        # TODO how to create communication? create 3 objects of creators?

    def __add_geo_information(self, country_id, language, region):
        try:
            self.geo_information = GeoInformation(
                country_id=country_id, language=language, region=region
            )
            db.session.add(self.geo_information)
            db.session.commit()
            self.geo_information_id = self.geo_information.id
        except:
            db.session.rollback()
            raise

    def add_attraction(
        self, name, description, photo_path, admin_id, google_maps=None, site_link=None
    ):
        try:
            attraction = Attraction(
                name=name,
                description=description,
                place_id=self.id,
                admin_id=admin_id,
                google_maps=google_maps,
                site_link=site_link,
            )
            self.attractions.append(attraction)
            db.session.add(attraction)
            db.session.commit()
            photo = Photo(attraction_id=attraction.id, photo_path=photo_path)
            db.session.add(photo)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def add_communication(self):
        # parameter which choose what kind of communication we want to add and then create
        # proper creator
        pass

    def add_weather(self):
        pass

    def add_hotel(
        self,
        name,
        country_id,
        city,
        street,
        nr_of_street,
        admin_id,
        nr_apartment=None,
        postcode=None,
        google_maps_link=None,
        site_link=None,
    ):
        try:
            address = Address(
                country_id=country_id,
                city=city,
                google_maps_link=google_maps_link,
                street=street,
                nr_of_street=nr_of_street,
                nr_of_apartment=nr_apartment,
                postcode=postcode,
            )
            db.session.add(address)
            db.session.commit()
            hotel = Hotel(
                name=name,
                address_id=address.id,
                place_id=self.id,
                admin_id=admin_id,
                site_link=site_link,
            )
            db.session.add(hotel)
            db.session.commit()
            return hotel, address
        except:
            db.session.rollback()
            return False

    def create_report(self, reporter_id, reason):
        try:
            report = PlaceReport(
                reporter_id=reporter_id, reason=reason, place_id=self.id
            )
            db.session.add(report)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    # TODO paginate
    @staticmethod
    def get_all_places():
        return Place.query.order_by(Place.note.desc())

    def add_visit(self, hotel_id, transport_id, name, start_date, end_date, user_id):
        try:
            visit = Visit(
                place_id=self.id,
                hotel_id=hotel_id,
                transport_id=transport_id,
                user_id=user_id,
                name=name,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.add(visit)
            db.session.commit()
            return visit
        except:
            db.session.rollback()
            return False

    def get_place_options(self):
        pass


class GeoInformation(db.Model):
    __tablename__ = "GeoInformation"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("Country.id"))
    language = db.Column(db.String(50))
    region = db.Column(db.String(50))


class Attraction(db.Model):
    __tablename__ = "Attraction"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"), nullable=False)
    description = db.Column(db.String(600), nullable=False)
    google_maps = db.Column(db.String(300))
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Integer, default=0)
    site_link = db.Column(db.String(400))
    admin_id = db.Column(db.Integer, db.ForeignKey("PlaceAdmin.id"), nullable=False)
    interested = db.relationship(
        "TypeOfInterests",
        secondary=attraction_interests,
        primaryjoin=(attraction_interests.c.attraction_id == id),
        secondaryjoin=(attraction_interests.c.interest_id == TypeOfInterests.id),
        backref=db.backref("attraction_interests", lazy="dynamic"),
        lazy="dynamic",
    )

    def add_comment(self):
        pass

    def add_photo(self):
        pass


class Photo(db.Model):
    __tablename__ = "Photo"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"))
    attraction_id = db.Column(db.Integer, db.ForeignKey("Attraction.id"))
    photo_path = db.Column(db.String(100), index=True)


class ProfilePhoto(db.Model):
    __tablename__ = "ProfilePhoto"

    id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String(100), index=True, nullable=False)


class Weather(db.Model):
    __tablename__ = "weather"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    cloudiness = db.Column(
        db.Integer
    )  # possible string, check what values we will accept here
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    date = db.Column(db.Date)

    def get_average_temperature(self):
        pass

    def show_weather_in_date_range(self):
        pass


class Address(db.Model):
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("Country.id"))
    city = db.Column(db.String(50), nullable=False)
    google_maps_link = db.Column(db.String(300))
    street = db.Column(db.String(100), nullable=False)
    nr_of_street = db.Column(db.String(10))
    nr_of_apartment = db.Column(db.Integer)
    postcode = db.Column(db.String(10))


class Hotel(db.Model):
    __tablename__ = "Hotel"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("Address.id"))
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Integer, default=0)
    site_link = db.Column(db.String(500))
    admin_id = db.Column(db.Integer, db.ForeignKey("PlaceAdmin.id"), nullable=False)


class Transport(db.Model):
    __tablename__ = "Transport"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("TypeOfTransport.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("Address.id"))
    name = db.Column(db.String(50))
    site_link = db.Column(db.String(300))
    admin_id = db.Column(db.Integer, db.ForeignKey("PlaceAdmin.id"), nullable=False)


class TypeOfTransport(db.Model):
    __tablename__ = "TypeOfTransport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Visit(db.Model):
    __tablename__ = "Visit"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    hotel_id = db.Column(db.Integer, db.ForeignKey("Hotel.id"))
    transport_id = db.Column(db.Integer, db.ForeignKey("Transport.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)
    attractions = db.relationship(
        "Attraction",
        secondary=visit_attractions,
        primaryjoin=(visit_attractions.c.visit_id == id),
        secondaryjoin=(visit_attractions.c.attraction_id == Attraction.id),
        backref=db.backref("visits", lazy="dynamic"),
        lazy="dynamic",
    )

    def add_post(self, text, photo_path, user_id):
        try:
            post = Post(
                text=text,
                creator_id=user_id,
                visit_id=self.id,
            )
            db.session.add(post)
            db.session.commit()
            db.session.commit()
            photo = Photo(photo_path=photo_path, post_id=post.id)
            db.session.add(post)
            db.session.commit()
            return post, photo
        except:
            db.session.rollback()
            return False

    def get_place(self):
        return Place.query.get(self.place_id)


class Settlement(db.Model):
    __tablename__ = "Settlement"

    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String, nullable=False, unique=True, index=True)


class PostReport(db.Model, Report):
    __tablename__ = "PostReport"

    id = db.Column(db.Integer, primary_key=True)
    moderator_id = db.Column(db.Integer, db.ForeignKey("Moderator.id"))
    settlement_id = db.Column(db.Integer, db.ForeignKey("Settlement.id"))
    reporter_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    interaction_id = db.Column(db.Integer, db.ForeignKey("Post.id"))
    reason = db.Column(db.String(200))
    creation_date = db.Column(db.Date, index=True)
    settlement_date = db.Column(db.Date, index=True)


    def __init__(
        self, reporter_id, reason, interaction_id, settlement_id=1, moderator_id=None
    ):
        super().__init__(
            reporter_id=reporter_id, reason=reason, settlement_id=settlement_id
        )
        self.moderator_id = moderator_id
        self.interaction_id = interaction_id
        self.creation_date = datetime.date.today()
        self.settlement_date = None


class CommentReport(db.Model, Report):
    __tablename__ = "CommentReport"

    id = db.Column(db.Integer, primary_key=True)
    moderator_id = db.Column(db.Integer, db.ForeignKey("Moderator.id"))
    settlement_id = db.Column(db.Integer, db.ForeignKey("Settlement.id"))
    reporter_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    interaction_id = db.Column(db.Integer, db.ForeignKey("Comment.id"))
    reason = db.Column(db.String(200))
    creation_date = db.Column(db.Date, index=True)
    settlement_date = db.Column(db.Date, index=True)

    def __init__(
        self, reporter_id, reason, interaction_id, settlement_id=1, moderator_id=None
    ):
        super().__init__(
            reporter_id=reporter_id, reason=reason, settlement_id=settlement_id
        )
        self.moderator_id = moderator_id
        self.interaction_id = interaction_id
        self.creation_date = datetime.date.today()
        self.settlement_date = None


class UserReport(db.Model, Report):
    __tablename__ = "UserReport"

    id = db.Column(db.Integer, primary_key=True)
    user_admin_id = db.Column(db.Integer, db.ForeignKey("UserAdmin.id"), default=None)
    settlement_id = db.Column(db.Integer, db.ForeignKey("Settlement.id"), default=1)
    reporter_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    reported_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    reason = db.Column(db.String(200))
    creation_date = db.Column(db.Date, index=True)
    settlement_date = db.Column(db.Date, index=True)

    def __init__(
        self, reporter_id, reason, reported_id, settlement_id=1, user_admin_id=None
    ):
        super().__init__(
            reporter_id=reporter_id, reason=reason, settlement_id=settlement_id
        )
        self.user_admin_id = user_admin_id
        self.reported_id = reported_id
        self.creation_date = datetime.date.today()
        self.settlement_date = None


class PlaceReport(db.Model, Report):
    __tablename__ = "PlaceReport"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("PlaceAdmin.id"))
    settlement_id = db.Column(db.Integer, db.ForeignKey("Settlement.id"))
    reporter_id = db.Column(db.Integer, db.ForeignKey("AppUser.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    reason = db.Column(db.String(200))
    creation_date = db.Column(db.Date, index=True)
    settlement_date = db.Column(db.Date, index=True)

    def __init__(self, reporter_id, reason, place_id, settlement_id=1, admin_id=None):
        super().__init__(
            reporter_id=reporter_id, reason=reason, settlement_id=settlement_id
        )
        self.admin_id = admin_id
        self.place_id = place_id
        self.creation_date = datetime.date.today()
        self.settlement_date = None


class Country(db.Model):
    __tablename__ = "Country"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(60), unique=True, nullable=False)

    @staticmethod
    def get_all_countries():
        return Country.query.all()


class ExperienceLevel(db.Model):
    __tablename__ = "ExperienceLevel"

    id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.String(60), unique=True, nullable=False)

    def add_experience_level_to_db(self):
        pass


class Sex(db.Model):
    __tablename__ = "Sex"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(7), unique=True, nullable=False)
