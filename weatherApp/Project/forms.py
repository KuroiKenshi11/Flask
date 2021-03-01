from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from wtforms import ValidationError
from .model import User
from flask import render_template


class Login(FlaskForm):
    email = StringField("Email ",  validators=[DataRequired(), Email()])
    password = PasswordField("Password ", validators=[DataRequired()])
    submit = SubmitField("Log in")


class Register(FlaskForm):
    email = StringField('Email ', validators=[DataRequired(), Email()])
    username = StringField('Username ', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('conf_pass', message='Passwords Must Match!')])
    conf_pass = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Register!')
    # Check if not None for that email!

    def check_email(self, email):
        return User.query.filter_by(email=email).first()
        # raise ValidationError(
        #     'Sorry, Your email has been registered already!')
    # Check if not None for that username!

    def check_username(self, username):
        return User.query.filter_by(username=username).first()
        # raise ValidationError(
        #     'Sorry, Your username has been registered already!')


class TempretureSearch(FlaskForm):
    search = StringField("")
    submit = SubmitField("Search")
