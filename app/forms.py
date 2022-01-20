from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    SubmitField
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


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
    email = StringField("email", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Enter User credentials")


class UserForm(FlaskForm):
    age = IntegerField("Age")
    city = StringField("City")
    country = StringField("Country")
    name = StringField("Name")
    sex = StringField("Sex")
    surname = StringField("Surname")
    submit = SubmitField("Enter User informations")


class InterestsForm(FlaskForm):
    business = BooleanField("Business")
    culture = BooleanField("Culture")
    entertainment = BooleanField("Entertainment")
    fashion = BooleanField("Fashion")
    gastronomy = BooleanField("Gastronomy")
    nature = BooleanField("Nature")
    sport = BooleanField("Sport")
    extreme_sport = BooleanField("Extreme Sport")
    water_sport = BooleanField("Water Sport")
