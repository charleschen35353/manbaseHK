from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField, Recaptcha
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, RadioField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from manbase.models import Users, BusinessUsers, IndividualUsers
from uuid import uuid4
from flask_login import current_user


# setting base error language as chinese
class BaseForm(FlaskForm):
    class Meta:
        locales = ['zh_TW']

class LoginForm(BaseForm):
    login = StringField('帳號',
                        validators=[DataRequired()])
    password = PasswordField('密碼',
                             validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('請記住我')
    submit = SubmitField('登入')

class CommentForm(BaseForm):
    comment = StringField('留言',
                           validators=[DataRequired(message = '留言不能為空'), Length(min=5, max=20)])
    submit = SubmitField('遞交留言')
class ResetPasswordForm(BaseForm):
    otp = PasswordField('one time password',
                             validators=[DataRequired()])
    password = PasswordField('密碼',
                             validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('重新輸入密碼',
                                     validators=[DataRequired(), EqualTo('password', message="必須與已輸入密碼相同")])
    submit = SubmitField('重置密碼')

class ForgetPasswordSelectionForm(BaseForm):
    selection =  RadioField('Retrieval Method', choices=[(1, "Login ID"), (2, "Contact Phone Number(Verified)"), (3, "Contact Us")],  
                            validators=[DataRequired()], coerce=int, default = 1)
   
    submit = SubmitField('Select')


class ForgetPasswordFormAccount(BaseForm):
    data = StringField('', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
    def validate_data(form, data):
        user = Users.query.filter_by(ur_login=data.data).first()
        if not user:
            raise ValidationError('此帳戶不存在。')

class ForgetPasswordFormPhone(BaseForm):
    data = StringField('', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
    def validate_data(form, data):
        user = Users.query.filter_by(ur_phone=data.data).first()
        if not user:
            raise ValidationError('此聯絡電話不存在。')

# Individual Users
# TODO: rewrite validators
class IndividualRegistrationForm(BaseForm):
    user_login = StringField('帳號',
                           validators=[DataRequired(message = '名字不能為空'), Length(min=5, max=20)])
    password = PasswordField('密碼',
                             validators=[DataRequired(message = '密碼不能為空'), Length(min=5, max=32)])
    #password validation 
    #TODO to be implemented on client side instead
    def password_requirement(form, field):
        # check if passwords contains 0-9 & a-z &A-Z and !@#$%
        # TODO
        if False:
            raise ValidationError(
                'Password must contain at least one number, one charater in upper case, one character in lower case, and a special character from \'@#!&*\'')
    confirm_password = PasswordField('重新輸入密碼',
                                     validators=[DataRequired(), EqualTo('password', message="必須與已輸入密碼相同")])
    individual_contact_number = IntegerField('聯絡電話',
                                        validators = [DataRequired(message = '聯絡電話不能為空')])
    individual_email = StringField('電子郵箱',
                                validators=[DataRequired(message = '電子郵箱不能為空'), Email()])
    individual_CName = StringField('中文全名',
                                validators = [DataRequired(message = '中文全名不能為空'), Length(min=1, max=20)])
    individual_EName = StringField('英文名字', validators = [])
    individual_alias = StringField('暱稱', validators = [])
    individual_HKID = StringField('身分證字母加首四位數字', validators = [DataRequired()])
    # DEBUG: removed validators
    individual_gender = RadioField('性別', choices=[(0, "女性"), (1, "男性"), (2, "保密")], validators=[], coerce=int)
    individual_birthday = DateField('出生日期', validators=[DataRequired()])
    # DEBUG: removed validators
    individual_educationLevel = RadioField('教育程度', choices=[(0, "小學畢業或以下"), (1, "完成中三"), (2, "中學畢業"), (3, "大學（本科）畢業"), (4, "大學（碩士或以上）畢業"), (5, "保密")], default=0, validators=[], coerce=int)
    individual_language_Cantonese = BooleanField('廣東話', validators=[])
    individual_language_English = BooleanField('英文', validators=[])
    individual_language_Putonghua = BooleanField('普通話', validators=[])
    individual_language_Other = StringField('其他', validators=[])
    individual_tos = BooleanField('使用條款及細則', validators=[DataRequired(message='您必須同意《使用條款及細則》。')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='您必須證明您不是機器人。請刷新頁面重新輸入。')])
    submit = SubmitField('註冊個人帳戶')


        
    def validate_user_login(form, user_login):
        user = Users.query.filter_by(ur_login=user_login.data).first()
        if user:
            raise ValidationError('此帳戶已存在，請登入。')

    def validate_individual_phone(form, individual_contact_number):
        user = Users.query.filter_by(ur_phone=individual_contact_number.data).first()
        if user:
            raise ValidationError('此電話號碼已存在，請重新輸入。')
    
    def validate_individual_email(form, individual_email):
        user = Users.query.filter_by(ur_email=individual_email.data).first()
        if user:
            raise ValidationError('此電郵已存在，請重新輸入。')

class IndividualUpdateProfileForm(BaseForm):

    individual_contact_number = IntegerField('聯絡電話')
    individual_email = StringField('電子郵箱')
    individual_CName = StringField('中文全名')
    individual_EName = StringField('英文名字')
    individual_alias = StringField('暱稱')
    individual_HKID = StringField('身分證字母加首四位數字')
    individual_educationLevel = RadioField('教育程度', choices=[(0, "小學畢業或以下"), (1, "完成中三"), (2, "中學畢業"), (3, "大學（本科）畢業"), (4, "大學（碩士或以上）畢業"), (5, "保密")], coerce=int)
    individual_language_Cantonese = BooleanField('廣東話',)
    individual_language_English = BooleanField('英文')
    individual_language_Putonghua = BooleanField('普通話')
    individual_language_Other = StringField('其他')
    individual_intro = TextAreaField('自我介紹')
    
    submit = SubmitField('更新個人帳戶')


class ChangePasswordForm(BaseForm):

    old_password = PasswordField('舊密碼')
    new_password = PasswordField('新密碼',
                             validators=[DataRequired(message = '密碼不能為空'), Length(min=5, max=32)])

    def password_requirement(form, field):
    # check if passwords contains 0-9 & a-z &A-Z and !@#$%
    # TODO
        if False:
            raise ValidationError(
                    'Password must contain at least one number, one charater in upper case, one character in lower case, and a special character from \'@#!&*\'')
    confirm_new_password = PasswordField('重新輸入新密碼',
                                 validators=[EqualTo('new_password', message="must match password")])
    submit = SubmitField('更新密碼')
       

class ApplyJobForm():
    submit = SubmitField('遞交申請')


# Business Users
class BusinessRegistrationForm(BaseForm):

    user_login = StringField('帳號',
                           validators=[DataRequired(message = '帳號不能為空'), Length(min=5, max=20)])
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
    
    # TODO: Invalid email address should have error messages in Traditional Chinese, not Simplified Chinese
    company_email = StringField('公司電子郵箱',
                                validators=[DataRequired(message = '公司電子郵箱不能為空'), Email()])
    business_tos = BooleanField('使用條款及細則', validators=[DataRequired(message='您必須同意《使用條款及細則》。')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='您必須證明您不是機器人。請刷新頁面重新輸入。')])
    submit = SubmitField('註冊商業帳戶')

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
        user = Users.query.filter_by(ur_email=company_email.data).first()
        if user:
            raise ValidationError(
                '此電郵已存在，請重新輸入。')

class BusinessUpdateProfileForm(BusinessRegistrationForm):
    company_address = StringField('公司地址',
                            validators=[])
    company_email = StringField('電子郵箱',
                                validators=[Email()])
    old_password = PasswordField('舊密碼',
                             validators=[])
    new_password = PasswordField('新密碼',
                             validators=[])
    confirm_new_password = PasswordField('重新輸入新密碼',
                             validators=[EqualTo('password', message="must match password")])
    submit = SubmitField('更新商業帳戶資料')

class PostJobForm(BaseForm):
    job_title = StringField('職位名稱',
                            validators=[DataRequired(message = '職位名稱不能為空')])
    job_description = StringField('工作內容',
                            validators=[DataRequired(message = '工作內容不能為空')])
    job_type = StringField('工作類型',
                            validators=[DataRequired(message = '工作類型不能為空')])
    job_expected_payment_days = IntegerField('預計出糧日期',
                                            validators=[DataRequired(message = '預計出糧日期不能為空')])
    list_start_time = DateTimeField('工作開始時間',
                                    validators=[DataRequired(message = '工作開始時間不能為空')])
    list_end_time = DateTimeField('工作完成時間',
                                    validators=[DataRequired(message = '工作完成時間不能為空')])
    list_salary = IntegerField('薪資',
                               validators=[DataRequired(message = '薪資不能為空')])
    list_salary_type = RadioField('薪資類別',
                                validators=[DataRequired(message = '薪資類別不能為空')])
    list_quota = IntegerField('職位空缺數目',
                            validators=[DataRequired(message = '職位空缺數目不能為空')])
    submit = SubmitField('遞交工作')
    
class AcceptApplicationForm():
    submit = SubmitField('確認申請')

class RateAndReviewOnIndividualForm():
    rating_score = RadioField('員工評分',
                        validators = [DataRequired(message = '員工評分不能為空')])
    comment = StringField('表現評價',
                        validators = [DataRequired(message = '表現評價不能為空')])
    submit = SubmitField('遞交評論')

class ConfirmAttendanceForm():
    status = RadioField('出席狀態',
                        validators = [DataRequired(message = '出席狀態不能為空')])
    submit = SubmitField('更新出席狀態')

class RateAndReviewOnBusinessForm():
    comment = StringField('留言',
                        validators = [DataRequired(message = '留言不能為空')])
    workload_score = RadioField('工作量評分',
                        validators = [DataRequired(message = '工作量分不能為空')])
    work_environment_score = RadioField('工作環境評分',
                        validators = [DataRequired(message = '工作環境評分不能為空')])
    administration_score = RadioField('管理人員評分',
                        validators = [DataRequired(message = '管理人員不能為空')])
    submit = SubmitField('遞交評論')

class ReportAbnormalityForm():
    message = StringField('問題描述',
                        validators = [DataRequired(message = '問題描述不能為空')])
    submit = SubmitField('錯誤報吿')

'''
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
                    'Email is taken. Please choose a different one')'''
