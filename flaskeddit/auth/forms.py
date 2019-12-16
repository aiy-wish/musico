import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email

from flaskeddit.models import AppUser


class RegisterForm(FlaskForm):
    """Form for registering a new user."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
            Length(min=6),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validates that a user with the given username does not already exist in the
        database.
        """
        app_user = AppUser.query.filter_by(username=username.data.lower()).first()
        if app_user is not None:
            raise ValidationError("Username is taken.")

    def validate_email(self, email):
        """
        Validates that a user with the given username does not already exist in the
        database.
        """
        app_user = AppUser.query.filter_by(email=email.data.lower()).first()
        if app_user is not None:
            raise ValidationError("Email is taken.")

    

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    token = StringField('Token', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = AppUser.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('That username does not exist in our database.')


    def validate_token(self, token):
        user = AppUser.query.filter_by(username=self.username.data).first()
        if user is not None and not user.verify_totp(token.data):
            raise ValidationError("Invalid Token")
