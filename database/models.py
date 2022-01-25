from app import db
from core.reports import ReportField, Report
from core.user_interaction import UserInteraction
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class AppUser(db.Model, ReportField, UserMixin):
    __tablename__ = "AppUser"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    experience = db.Column(db.Integer)
    experience_level_id = db.Column(db.Integer, db.ForeignKey('ExperienceLevel.id'))
    personal_info_id = db.Column(db.Integer, db.ForeignKey('PersonalInfo.id'))
    password_hash = db.Column(db.String(128))

    __mapper_args__ = {
        'polymorphic_identity': 'AppUser',
        'polymorphic_on': login
    }

    def __init__(self, login, email):
        self.login = login
        self.email = email

    def __repr__(self):
        return f"user: {self.username}"

    def create_report(self):
        pass

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


user_interests = db.Table(
    'user_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('AppUser.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('TypeOfInterests.id')),
    db.PrimaryKeyConstraint('user_id', "interest_id", name='user_interest_id')
)


class PersonalInfo(db.Model):
    __tablename__ = "PersonalInfo"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    name = db.Column(db.String(40))
    sex_id = db.Column(db.Integer, db.ForeignKey('Sex.id'))
    surname = db.Column(db.String(80))


class Moderator(AppUser, db.Model):
    __tablename__ = "Moderator"

    id = db.Column(db.Integer, db.ForeignKey('AppUser.id'), primary_key=True)


class UserAdmin(AppUser):
    __tablename__ = "UserAdmin"

    id = db.Column(db.Integer, db.ForeignKey('AppUser.id'), primary_key=True)


class PlaceAdmin(AppUser):
    __tablename__ = "PlaceAdmin"

    id = db.Column(db.Integer, db.ForeignKey('AppUser.id'), primary_key=True)


class Post(db.Model, UserInteraction):
    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey('Visit.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    creation_date = db.Column(db.DateTime)
    text = db.Column(db.String(2000))
    note = db.Column(db.Integer)

    def __init__(self, creator_id):
        self.creator_id = creator_id

    def create_report(self):
        pass


class Comment(db.Model, UserInteraction):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    creation_date = db.Column(db.DateTime)
    text = db.Column(db.String(500))
    given_note = db.Column(db.Integer)

    def create_report(self):
        pass


class Place(db.Model, ReportField):
    __tablename__ = "Place"

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    name = db.Column(db.String(40), index=True, unique=True)
    geo_information_id = db.Column(db.Integer, db.ForeignKey('GeoInformation.id'))

    def __init__(self, place_admin):
        self.attractions = []
        self.communication = []
        self.hotels = []
        self.place_admin = place_admin
        self.average_weather = None  # TODO think how show the weather
        # TODO how to create communication? create 3 objects of creators?

    def add_geo_information(self):
        self.geo_information = GeoInformation()
        # TODO add db record with geoinformation, take somehow id
        # self.geo_information_id = received_id

    def add_attraction(self):
        pass

    def add_communication(self):
        # parameter which choose what kind of communication we want to add and then create
        # proper creator
        pass

    def add_weather(self):
        pass

    def add_hotel(self):
        pass


class GeoInformation(db.Model):
    __tablename__ = "GeoInformation"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Integer, db.ForeignKey('Country.id'))
    language = db.Column(db.String(50))
    region = db.Column(db.String(50))


class Attraction(db.Model):
    __tablename__ = "Attraction"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    description = db.Column(db.String(600), nullable=False)
    google_maps = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Integer, nullable=False)
    site_link = db.Column(db.String(150))

    def __init__(self):
        self.photos = []
        self.comments = []
        # get all comments and photo with constraint id

    def add_comment(self):
        pass

    def add_photo(self):
        pass


attraction_interests = db.Table(
    'attraction_interests',
    db.Column('attraction_id', db.Integer, db.ForeignKey('Attraction.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('TypeOfInterests.id')),
    db.PrimaryKeyConstraint('attraction_id', "interest_id", name='attraction_interest_id')
)


class Photo(db.Model):
    __tablename__ = "Photo"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    attraction_id = db.Column(db.Integer, db.ForeignKey('Attraction.id'))
    photo_path = db.Column(db.String(100), index=True)


class Weather(db.Model):
    __tablename__ = "weather"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    cloudiness = db.Column(db.Integer)  # possible string, check what values we will accept here
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    date = db.Column(db.Date)

    def get_average_temperature(self):
        pass

    def show_weather_in_date_range(self):
        pass


class Address(db.Model):
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    city = db.Column(db.String(50), nullable=False)
    google_maps_link = db.Column(db.String(150))
    street = db.Column(db.String(100), nullable=False)
    nr_of_street = db.Column(db.Integer)
    nr_of_apartment = db.Column(db.Integer)
    postcode = db.Column(db.String(10))


class Hotel(db.Model):
    __tablename__ = "Hotel"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('Address.id'))
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Integer, nullable=False)
    site_link = db.Column(db.String(100))


class Transport(db.Model):
    __tablename__ = "Transport"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('TypeOfTransport.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('Address.id'))
    name = db.Column(db.String(50))
    site_link = db.Column(db.String(100))


class TypeOfTransport(db.Model):
    __tablename__ = "TypeOfTransport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Visit(db.Model):
    __tablename__ = "Visit"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotel.id'))
    transport_id = db.Column(db.Integer, db.ForeignKey('Transport.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __init__(self):
        pass


visit_attractions = db.Table(
    'visit_attractions',
    db.Column('visit_id', db.Integer, db.ForeignKey('Visit.id')),
    db.Column('attraction_id', db.Integer, db.ForeignKey('Attraction.id')),
    db.PrimaryKeyConstraint('visit_id', "attraction_id", name='visit_attraction_id')
)


class Settlement(db.Model):
    __tablename__ = "Settlement"

    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String, nullable=False, unique=True, index=True)


class PostReport(db.Model, Report):
    __tablename__ = "PostReport"

    id = db.Column(db.Integer, primary_key=True)
    moderator_id = db.Column(db.Integer, db.ForeignKey('Moderator.id'))
    settlement = db.Column(db.Integer, db.ForeignKey('Settlement.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    reason = db.Column(db.String(200))

    def __init__(self, reporter_id, reason, post_id, settlement=None, moderator_id=None):
        super().__init__(reporter_id=reporter_id, reason=reason, settlement=settlement)
        self.moderator_id = moderator_id
        self.post_id = post_id

    # TODO
    def consider(self, settlement, moderator_id):
        self.settlement = settlement
        self.moderator_id = moderator_id


class CommentReport(db.Model, Report):
    __tablename__ = "CommentReport"

    id = db.Column(db.Integer, primary_key=True)
    moderator_id = db.Column(db.Integer, db.ForeignKey('Moderator.id'))
    settlement = db.Column(db.Integer, db.ForeignKey('Settlement.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('Comment.id'))
    reason = db.Column(db.String(200))

    def __init__(self, reporter_id, reason, comment_id, settlement=None, moderator_id=None):
        super().__init__(reporter_id=reporter_id, reason=reason, settlement=settlement)
        self.moderator_id = moderator_id
        self.comment_id = comment_id

    # TODO
    def consider(self, settlement, moderator_id):
        self.settlement = settlement
        self.moderator_id = moderator_id


class UserReport(db.Model, Report):
    __tablename__ = "UserReport"

    id = db.Column(db.Integer, primary_key=True)
    user_admin_id = db.Column(db.Integer, db.ForeignKey('UserAdmin.id'))
    settlement = db.Column(db.Integer, db.ForeignKey('Settlement.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    reported_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    reason = db.Column(db.String(200))

    def __init__(self, reporter_id, reason, reported_id, settlement=None, user_admin_id=None):
        super().__init__(reporter_id=reporter_id, reason=reason, settlement=settlement)
        self.user_admin_id = user_admin_id
        self.reported_id = reported_id

    # TODO
    def consider(self, settlement, user_admin_id):
        self.settlement = settlement
        self.user_admin_id = user_admin_id


class PlaceReport(db.Model, Report):
    __tablename__ = "PlaceReport"

    id = db.Column(db.Integer, primary_key=True)
    place_admin_id = db.Column(db.Integer, db.ForeignKey('PlaceAdmin.id'))
    settlement = db.Column(db.Integer, db.ForeignKey('Settlement.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('AppUser.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))
    reason = db.Column(db.String(200))

    def __init__(self, reporter_id, reason, place_id, settlement=None, place_admin_id=None):
        super().__init__(reporter_id=reporter_id, reason=reason, settlement=settlement)
        self.place_admin_id = place_admin_id
        self.place_id = place_id

    # TODO
    def consider(self, settlement, place_admin_id):
        self.settlement = settlement
        self.place_admin_id = place_admin_id

class Country(db.Model):
    __tablename__ = "Country"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(60), unique=True, nullable=False)


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


class TypeOfInterests(db.Model):
    __tablename__ = "TypeOfInterests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
