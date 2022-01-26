from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    MultipleFileField
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, URL
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import photos


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=4, max=30),
        EqualTo('password_2', message="Passwords must match")])
    password_2 = PasswordField("Repeat Password", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Length(min=4, max=15), Email()])
    submit = SubmitField("Enter User credentials")

    def validate_username(self, username):
        user = AppUser.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = AppUser.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UserForm(FlaskForm):
    age = IntegerField("Age", validators=[NumberRange(min=10, max=100)])
    city = StringField("City")
    country = StringField("Country")
    name = StringField("Name", validators=[DataRequired()])
    sex = StringField("Sex", SelectField('choose your Gender', choices=['Male', 'Female']))  # TODO take from db
    surname = StringField("Surname")
    submit = SubmitField("Enter User informations")


class InterestsForm(FlaskForm):
    # business = BooleanField("Business")
    # culture = BooleanField("Culture")
    # entertainment = BooleanField("Entertainment")
    # fashion = BooleanField("Fashion")
    # gastronomy = BooleanField("Gastronomy")
    # nature = BooleanField("Nature")
    # sport = BooleanField("Sport")
    # extreme_sport = BooleanField("Extreme Sport")
    # water_sport = BooleanField("Water Sport")
    interests = SelectMultipleField() # TODO think how


class PostForm(FlaskForm):
    text = StringField("Describe your adventures", validators=[DataRequired(), Length(min=1, max=2000)])
    photo = MultipleFileField("Photo of attraction",
                      validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])


class CommentForm(FlaskForm):
    text = StringField("Describe your adventures", validators=[DataRequired(), Length(min=1, max=200)])
    given_note = IntegerField("What is your note of post", NumberRange(min=-2, max=2))
