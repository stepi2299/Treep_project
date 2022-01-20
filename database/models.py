from app import db


class AppUser(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    experiance = db.Column(db.Integer)
    #experiance_level = db.Column(db.)
    # interests = db.Columns
    personal_info_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"user: {self.username}"


class PersonalInfo(db.Model):
    __tablename__ = "personal_info"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), index=True)
    #country = db.Column()
    name = db.Column(db.String(40))
    #sex
    surname = db.Column(db.String(80))

