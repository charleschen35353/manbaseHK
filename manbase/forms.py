from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from manbase.models import Users, BusinessUsers
from uuid import uuid4

def password_requirement(form, field):
    # check if passwords contains 0-9 & a-z &A-Z and !@#$%
    # TODO
    if False:
        raise ValidationError(
            'Password must contain at least one number, one charater in upper case, one character in lower case, and a special character from \'@#!&*\'')

#setting base error language as chinese
class BaseForm(FlaskForm):
    class Meta:
        locales = ['zh']

class LoginForm(BaseForm):

    login = StringField('帳號',
                        validators=[DataRequired()])
    password = PasswordField('密碼',
                             validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('請記住我')
    submit = SubmitField('登入')

#Individual Users
class IndividualRegistrationForm(BaseForm):

    user_login = StringField('帳號',
                           validators=[DataRequired(message = '名字不能為空'), Length(min=5, max=20)])
    password = PasswordField('密碼',
                             validators=[DataRequired(message = '密碼不能為空'), Length(min=5, max=32)])
    confirm_password = PasswordField('重新輸入密碼',
                                     validators=[DataRequired(), EqualTo('password', message="必須與已輸入密碼相同")])
    individual_contact_number = IntegerField('聯絡電話',
                                        validators = [DataRequired(message = '聯絡電話不能為空')])
    individual_email = StringField('電子郵箱',
                                validators=[DataRequired(message = '電子郵箱不能為空'), Email()])
    individual_CName = StringField('中文全名',
                                validators = [DataRequired(message = '中文全名不能為空'), Length(min=1, max=20)])
    individual_EName = StringField('英文名字',
                                validators = [])
    individual_alias = StringField('暱稱',
                                validators = [])
    individual_HKID_head = StringField('身分證首字母',
                                validators = [DataRequired()])
    individual_HKID_tail = StringField('身分證後三位',
                                validators = [DataRequired(), Length(min=3, max=3)])
    individual_gender = IntegerField('性別', validators=[DataRequired()])
    individual_birthday = DateField('出生日期', validators=[DataRequired()])
    individual_educationLevel = StringField('教育程度',
                                    validators=[])
    individual_language_Cantonese = IntegerField('工作語言 - 廣東話', validators=[])
    individual_language_English = IntegerField('工作語言 - 英文', validators=[])
    individual_language_Putonghua = IntegerField('工作語言 - 普通話', validators=[])
    individual_language_Other = IntegerField('工作語言 - 其他', validators=[])

    submit = SubmitField('註冊個人帳戶')

    def validate_user_login(self, user_login):
        user = Users.query.filter_by(ur_login=user_login.data).first()
        if user:
            raise ValidationError(
                '此帳戶已存在，請登入。')

    def validate_individual_phone(self, company_CName):
        user = IndividualUsers.query.filter_by(iu_phone=individual_contact_number.data).first()
        if user:
            raise ValidationError(
                '此電話號碼已存在，請重新輸入。')
    
    def validate_company_email(self, company_email):
        user = IndividualUsers.query.filter_by(iu_email=individual_email.data).first()
        if user:
            raise ValidationError(
                '此個人電郵已存在，請重新輸入。')

class UpdateAccountForm(BaseForm):

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
class BusinessRegistrationForm(BaseForm):

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