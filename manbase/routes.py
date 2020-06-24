import secrets
import os
import cv2
import matplotlib.image as pltimg
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user , current_user, login_required
from manbase import app, db, bcrypt, login_manager
from manbase.forms import BusinessRegistrationForm,IndividualRegistrationForm, LoginForm, UpdateAccountForm
from manbase.models import Users, BusinessUsers, IndividualUsers
from datetime import datetime
from uuid import uuid4

posts = [ #fake db return
	{
		'author': "Charles Chen",
		'title': "Home Page Prototype",
        	'content': "This is the home page of ManBase",
       		'date_posted': "May 6, 2020",
	} 
]

@login_manager.user_loader
def load_user(ur_id):
    return Users.query.get(ur_id)

# =======================================
#           ROUTE DEFINITIONS
# =======================================

# @ROUTE DEFINTION
# NAME:     Public Homepage
# PATH:     /
# METHOD:   GET
# DESC.:    The homepage where the public will see
# @ROUTE DEFINTION
# NAME:     Member Homepage (TODO)
# PATH:     /
# METHOD:   GET
# DESC.:    The homepage where the member will see
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        # TODO: Get the user info and render it into the homepage
        return render_template('home.html', posts=posts)
    else:
        return render_template('index.html')

# @ROUTE DEFINTION
# NAME:     About Page
# PATH:     /about
# METHOD:   GET
# DESC.:    The about page of the website
@app.route('/about')
def about():
    return render_template('about.html', title = "about us")

# @ROUTE DEFINTION
# NAME:     Login Page
# PATH:     /login
# METHOD:   GET / POST
# DESC.:    [GET]   The login form for public to use
#           [POST]  The method which validates the user's credential
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(ur_login=form.login.data).first()
        
        if user and bcrypt.check_password_hash(user.ur_password_hash, form.password.data):
            login_user(user, remember = form.remember.data)
            flash("成功登入.".format(form.login.data),"success")
            return redirect(url_for('home'))
        else:
            flash('登入失敗. 請重新檢查帳號或密碼.', 'fail')
    return render_template('login.html', title='Login', form=form)

# @ROUTE DEFINTION
# NAME:     Logout
# PATH:     /logout
# METHOD:   GET
# DESC.:    The method which logs the user out
@app.route('/logout')
def logout():
    logout_user()
    flash('您已成功登出.', 'success')
    return redirect(url_for('home'))

# @ROUTE DEFINTION
# NAME:     Logout
# PATH:     /register
# METHOD:   GET
# DESC.:    The page where the user selects whether they need 
#           a business account or an individual account
@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('register.html', title='註冊')

# @ROUTE DEFINTION
# NAME:     Registration (Individual)
# PATH:     /individual_register
# METHOD:   GET / POST
# DESC.:    [GET]   The page where the individual user creates their account
#           [POST]  The method which validates the registration info and register the user
@app.route("/individual_register",methods=['GET', 'POST'])
def individual_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = IndividualRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        uid = str(uuid4())

        # Ensure the generated user ID is unique
        validate_uid = Users.query.filter_by(ur_id=uid).first()
        while validate_uid:
            uid = str(uuid4())
            validate_uid = Users.query.filter_by(ur_id=uid).first()

        user = Users(
                    ur_creationTime = datetime.utcnow(), 
                    ur_id = uid,
                    ur_login = form.user_login.data,
                    ur_password_hash = hashed_password
                    )
        individual_user = IndividualUsers(
                                    iu_id = uid,
                                    iu_phone = form.individual_contact_number.data,
                                    iu_email = form.individual_email.data,
                                    iu_CName = form.individual_CName.data,
                                    iu_EName = form.individual_EName.data,
                                    iu_alias = form.individual_alias.data,
                                    iu_HKID = form.individual_HKID.data,
                                    iu_gender = form.individual_gender.data,
                                    iu_birthday = form.individual_birthday.data,
                                    iu_educationLevel = form.individual_educationLevel.data,
                                    iu_language_Cantonese = form.individual_language_Cantonese.data,
                                    iu_language_English = form.individual_language_English.data,
                                    iu_language_Putonghua = form.individual_language_Putonghua.data,
                                    iu_language_Other = form.individual_language_Other.data
                                    )
        db.session.add(user)
        db.session.add(individual_user)
        db.session.commit()

        flash(f'{form.individual_CName.data} 的個人帳號已成功註冊!', 'success')
        return redirect(url_for('home'))
    return render_template('individual_register.html', title='註冊 - 個人帳戶', form = form)

# @ROUTE DEFINTION
# NAME:     Registration (Business)
# PATH:     /business_register
# METHOD:   GET / POST
# DESC.:    [GET]   The page where the business user creates their account
#           [POST]  The method which validates the registration info and register the user
@app.route("/business_register",methods=['GET', 'POST'])
def business_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = BusinessRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        uid = str(uuid4())

        # Ensure the generated user ID is unique
        validate_uid = Users.query.filter_by(ur_id=uid).first()
        while validate_uid:
            uid = str(uuid4())
            validate_uid = Users.query.filter_by(ur_id=uid).first()

        user = Users(
                    ur_creationTime = datetime.utcnow(), 
                    ur_id = uid,
                    ur_login = form.user_login.data,
                    ur_password_hash = hashed_password
                    )
        business_user = BusinessUsers(
                                    bu_id = uid,
                                    bu_address = 'NS', #not specified
                                    bu_CName = form.company_CName.data,
                                    bu_EName = form.company_EName.data,
                                    bu_picName = form.company_contact_person.data,
                                    bu_phone = form.company_contact_number.data
                                    )
        db.session.add(user)
        db.session.add(business_user)
        db.session.commit()

        flash(f'{form.company_CName.data} 的商業帳號已成功註冊!', 'success')
        return redirect(url_for('home'))
    return render_template('business_register.html', title='註冊 - 商業帳戶', form = form)

# =======================================
#    INCOMPLETED / SUSPENDED ROUTES
# =======================================

def save_picture(form_picture):
    """
    A utility function which helps save the profile picture in 'static/profile_pics',
    and return the new name of the profile picture
    """
    # Rename the profile picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the picture and save it in the path
    img = pltimg.imread(form_picture)
    img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(picture_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return picture_fn

# @ROUTE DEFINTION
# NAME:     Update Account Info
# PATH:     /account
# METHOD:   GET / POST
# DESC.:    TBC
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn = save_picture(form.picture.data)
            current_user.profile_image = picture_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        # TODO: Update the new information on the remote database
        '''db.session.commit()'''
        flash("Account Info Updated")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.profile_image)
    return render_template('account.html', title='account', image_file = image_file, form = form)

# @ROUTE DEFINTION
# NAME:     Confirm Business Registration
# PATH:     /business_register_confirm
# METHOD:   TBC
# DESC.:    TBC
@app.route('/business_register_confirm', methods=['GET','POST'])
def business_register_confirm():
    return render_template('business_register_confirm.html',title = '註冊 - 商業帳戶資料確認')

# =======================================
#             ERROR HANDLERS
# =======================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500