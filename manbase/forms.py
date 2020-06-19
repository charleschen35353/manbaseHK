from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from manbase.models import Users, BusinessUsers
from uuid import uuid4

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
        user = users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username is taken. Please choose a different one')

    def validate_email(self, email):
        user = users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email is taken. Please choose a different one')


class LoginForm(FlaskForm):

    login = StringField('帳號',
                        validators=[DataRequired()])
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
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Email is taken. Please choose a different one')


'''business'''
class BusinessRegistrationForm(FlaskForm):

    user_login = StringField('帳號',
                           validators=[DataRequired(message = '名字不能為空'), Length(min=5, max=20)])
    password = PasswordField('密碼',
                             validators=[DataRequired(message = '密碼不能為空'), Length(min=5, max=32)])
    confirm_password = PasswordField('重新輸入密碼',
                                     validators=[DataRequired(), EqualTo('password', message="must match password")])
    company_CName = StringField('企業中文名字',
                                validators = [DataRequired(message = '企業中文名字不能為空'), Length(min=1, max=20)])
    company_EName = StringField('企業英文名字',
                                validators = [])

    company_contact_person = StringField('聯絡人',
                                        validators = [DataRequired(message = '公司聯絡人不能為空'), Length(min=1,max=32)])
    company_contact_number = IntegerField('聯絡電話',
                                        validators = [DataRequired(message = '聯絡電話不能為空')])
    company_email = StringField('公司電子郵箱',
                                validators=[DataRequired(message = '公司電子郵箱不能為空'), Email()])

    submit = SubmitField('註冊')

    def validate_user_login(self, user_login):
        user = Users.query.filter_by(ur_login=user_login.data).first()
        if user:
            raise ValidationError(
                '此商業帳戶已存在，請登入。')

    def validate_company_CName(self, company_CName):
        user = BusinessUsers.query.filter_by(bu_CName=company_CName.data).first()
        if user:
            raise ValidationError(
                '此商業名稱已存在，請重新輸入。')

    
    def validate_company_email(self, company_email):
        user = BusinessUsers.query.filter_by(bu_email=company_email.data).first()
        if user:
            raise ValidationError(
                '此企業電郵已存在，請重新輸入。')