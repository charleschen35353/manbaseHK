import secrets
import os
import cv2
import matplotlib.image as pltimg
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user , current_user, login_required
from manbase import app, db, bcrypt, login_manager
from manbase.forms import BusinessRegistrationForm,IndividualRegistrationForm, LoginForm, UpdateAccountForm, PostJobForm
from manbase.models import Users, BusinessUsers, IndividualUsers, Jobs, JobListings
from datetime import datetime
from uuid import uuid4

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
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        # TODO: Get the user info and render it into the homepage
        uid = current_user.get_id()
        if BusinessUsers.query.filter_by(bu_id = uid).first():
            return redirect(url_for('business_home'))
        elif IndividualUsers.query.filter_by(iu_id = uid).first():
            return redirect(url_for('individual_home'))
        else:
            return render_template('home.html', posts=posts)
    else:
        return render_template('index.html')
    
# @ROUTE DEFINTION
# NAME:     Business Homepage
# PATH:     /home_business
# METHOD:   GET
# DESC.:    The homepage where the business user will see
@app.route('/home/business')
@login_required
def business_home():
    if BusinessUsers.query.filter_by(bu_id = current_user.get_id()).first():
        return render_template('business_home.html')
    else:
        return render_template('404.html'), 404

# @ROUTE DEFINTION
# NAME:     Individual Homepage
# PATH:     /home_individual
# METHOD:   GET
# DESC.:    The homepage where the individual user will see
@app.route('/home/individual')
@login_required
def individual_home():
    if IndividualUsers.query.filter_by(iu_id = current_user.get_id).first():
        return render_template('individual_home.html')
    else:
        return render_template('404.html'), 404

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
@app.route("/register/individual",methods=['GET', 'POST'])
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
@app.route("/register/business",methods=['GET', 'POST'])
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

# @ROUTE DEFINTION
# NAME:     Registration (Business)
# PATH:     /business_post_job
# METHOD:   GET / POST
# DESC.:    [GET]   The page where the business user creates their account
#           [POST]  The method which validates the job info and post a job
#TODO:need to validate user type: business user
@app.route("/business/job/new",methods=['GET', 'POST'])
@login_required
def business_post_job():

    if BusinessUsers.query.filter_by(bu_id = current_user.get_id()).first():
        return render_template('404.html'), 404

    form = PostJobForm()

    if current_user.is_authenticated:
            return redirect(url_for('home'))

    if form.validate_on_submit():

        jid = str(uuid4())

        # Ensure the generated job ID is unique
        validate_jid = Jobs.query.filter_by(jb_id=jid).first()
        while validate_jid:
            uid = str(uuid4())
            validate_jid = Jobs.query.filter_by(jb_id=jid).first()

        job = Jobs(
                jb_creationTime = datetime.utcnow(),
                jb_id = jid,
                jb_title = form.job_title.data,
                jb_description = form.job_description.data,
                jb_expected_payment_days = form.job_expected_payment_days.data,
                jb_bu_id = current_user.get_id(),
                jb_jt_id = form.job_type.data,
        )

        liid = str(uuid4())

        # Ensure the generated job listing ID is unique
        validate_liid = Jobs.query.filter_by(li_id = llid).first()
        while validate_liid:
            uid = str(uuid4())
            validate_liid = Jobs.query.filter_by(li_id = llid).first()

        job_list = JobListings(
                li_id = liid,
                li_jb_id = jid,
                li_starttime = form.list_start_time.data,
                li_endtime = form.list_end_time.data,
                li_salary_amt = form.list_salary.data,
                li_salary_type = form.list_salary_type.data,
                li_quota = form.list_quota.data
        )

        db.session.add(job)
        db.session.add(job_list)
        db.session.commit()

        flash(f'您的工作已成功發布!', 'success')
        return redirect(url_for('home'))

    return render_template('business_post_job.html', title = '發布工作', form = form)

# @ROUTE DEFINTION
# NAME:     View Job Posted
# PATH:     /business/jobs
# METHOD:   GET
# DESC.:    The page where the user selects whether they need 
#           a business account or an individual account
@app.route("/business/jobs",methods=['GET', 'POST'])
@login_required
def business_view_jobs_posted():
    if BusinessUsers.query.filter_by(bu_id = current_user.get_id()).first():
        return render_template('404.html'), 404
    jobs = Jobs.query.filter_by(jb_bu_id = current_user.get_id()).all()
    return render_template('business_jobs_posted.html', title="已發布的工作", jobs = jobs)

# @ROUTE DEFINTION
# NAME:     View Specific Job
# PATH:     /business/jobs/<job_id>
# METHOD:   GET
# DESC.:    The page where the business user view a specific job posted
@app.route('business/jobs/<job_id>')
@login_required
def job(job_id):
    job = Jobs.query.get_or_404(job_id)
    listings = JobListings.query.filter_by(li_jb_id=job.jb_id).all()
    return render_template('business_job.html',title=job.jb_title, job = job, listings = listings)

    if job.jb_bu_id != current_user:
        abort(403)
    


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
@app.route('/business/register/confirm', methods=['GET','POST'])
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