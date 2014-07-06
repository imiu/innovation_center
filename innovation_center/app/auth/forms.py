from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from .models import User
from flask.ext.login import current_user


class LoginForm(Form):
    """ a form to log in the user if their account exists """
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    """ the form to register a new user who does not yet have an account """
    email = StringField('Email', validators=[
        Required(), Email()
    ])
    username = StringField('Username', validators=[
        Required()
    ])
    first_name = StringField('First Name', validators=[
        Required()
    ])
    last_name = StringField('Last Name', validators=[
        Required()
    ])
    password = PasswordField('Password', validators=[
        Required(),
        EqualTo('confirm_password', message='Your passwords did not match'),
        Length(min=6, max=20, message='passwords must be longer than 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        Required()
    ])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """ confirm the email isn't already registered """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Invalid Login')

    def validate_username(self, field):
        """ confirm the username is not already in use, as this will be the link to their profile """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')