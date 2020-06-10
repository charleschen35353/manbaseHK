from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from manbase.models import User


def password_requirement(form, field):
    # check if passwords contains 0-9 & a-z &A-Z and !@#$%
    # TODO
    if False:
        raise ValidationError(
            'Password must contain at least one number, one charater in upper case, one character in lower case, and a special character from \'@#!&*\'')


class RegistrationForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5, max=32)])
    confirm_password = PasswordField('Comfirm Password',
                                     validators=[DataRequired(), EqualTo('password', message="must match password")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email is taken. Please choose a different one')


class LoginForm(FlaskForm):

    email = StringField('電郵',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密碼',
                             validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('請記住我')
    submit = SubmitField('登入')


class UpdateAccountForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Updtae Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Email is taken. Please choose a different one')
