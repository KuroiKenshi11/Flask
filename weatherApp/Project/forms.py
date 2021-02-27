from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from wtforms import ValidationError
from .model import User


class Login(FlaskForm):
    email = StringField("Email: ",  validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log in")


class Register(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    username = StringField('Username: ', validators=[DataRequired()])
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

    def check_email(self, email):
        # Check if not None for that user email!
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, username):
        # Check if not None for that username!
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Sorry, that username is taken!')


class TempretureSearch(FlaskForm):
    search = StringField("")
    submit = SubmitField("Search")
