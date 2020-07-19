import secrets
import os
import cv2
import matplotlib.image as pltimg
import secrets
import math
import random
from flask import render_template, url_for, flash, redirect, request, abort, Markup
from flask_login import login_user, logout_user , current_user, login_required
from flask_mail import Message
from manbase import app, db, bcrypt, login_manager, mail
from manbase.forms import *
from manbase.models import *
from datetime import datetime
from uuid import uuid4
from collections import defaultdict 
from manbase.utils import *

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
            return render_template('home.html')
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
    if IndividualUsers.query.filter_by(iu_id = current_user.get_id()).first():
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
    

@app.route('/register/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token_for(token, "email")
    except:
        flash('The confirmation link is invalid or has expired. Please request again through personal profile page.', 'danger')
        return redirect(url_for('home'))
        
    user = Users.query.filter_by(ur_email=email).first_or_404()
    if user.ur_isEmailVerified:
        flash('Account already confirmed. Please login or keep browsing.', 'success')
    else:
        user.ur_isEmailVerified = True
        user.ur_email_key = None
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))


@app.route('/request_confirmation_email/<string:uid>', methods = ['GET'])
def request_confirmation_email(uid):
    #uid always exists
    user = Users.query.filter_by(ur_id = uid).first()
    try:
        token = generate_confirmation_token_for(user, "email")
    except:
        return redirect(url_for('500'))
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.ur_email, subject, html)
    flash("Confirmation Email Sent.","success")
    return redirect(url_for('home'))


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

@app.route('/reset_password/<token>',  methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    email = False
    try:
        email = confirm_token_for(token, "reset")
    except:
        flash(Markup('The confirmation link is invalid or has expired. Please request again <a href={} class="alert-link"> here </a>'.format(url_for('forget_password_selection'))), 'danger')
        return redirect(url_for("home"))

    if email:
        user = Users.query.filter_by(ur_email=email).first()
    else:
        flash('Token is invalid or expired.', 'fail')
        return redirect(url_for("home"))

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.ur_otp_hash,form.otp.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.ur_password_hash = hashed_password
            user.ur_otp_hash = None
            db.session.commit()
            flash('You have successfully reset your password!', 'success')
            return redirect(url_for('login'))
        else:
             flash('Incorrect OTP!', 'fail')

    return render_template("reset_password.html", form = form)



@app.route('/forget_password/<string:selection>', methods=['GET', 'POST'])
def forget_password(selection):
    form = None
    if selection == "Contact":
        return redirect(url_for("contact us"))    
    elif selection == "Account":
        form = ForgetPasswordFormAccount()
    elif selection == 'Phone':
        form = ForgetPasswordFormPhone()
    else:
        return redirect(url_for("404"))

    if form.validate_on_submit():
        data = form.data.data 
        
        if selection == "Account":
            #retrieve email via login
            user = Users.query.filter_by(ur_login = data).first()

        elif selection == 'Phone':
            user = Users.query.filter_by(ur_phone = data).first()
              
        length = len(app.config['DEFAULT_STRING']) 
        otp = ""
        for i in range(6) : 
            otp += app.config['DEFAULT_STRING'] [math.floor(random.random() * length)] 

        try:
            token = generate_confirmation_token_for(user, "reset")
        except:
            return redirect(url_for('500'))
            
        reset_url = url_for('reset_password', token=token, _external=True)
        html = render_template('reset_password_email.html', reset_url=reset_url, otp = otp)
        subject = "Your email for password reset"
        send_email(user.ur_email, subject, html)
       
        user.ur_otp_hash = bcrypt.generate_password_hash(otp).decode('utf-8')
        db.session.commit()
        flash("您的密碼重置郵件已發送至您的電子信箱內.","success")
        return redirect(url_for('home'))
    return render_template('forget_password.html', title='忘記密碼', form = form, method = selection)

@app.route('/forget_password_selection', methods=['GET', 'POST'])
def forget_password_selection():
    form = ForgetPasswordSelectionForm()

    if form.validate_on_submit():
        selection = None
        if form.selection.data == 1:
            selection = 'Account'
        elif form.selection.data == 2:
            selection = 'Phone' 
        elif form.selection.data == 3:
            selection = 'Contact'
        return redirect(url_for('forget_password', selection = selection))
    return render_template('forget_password_selection.html', title='忘記密碼', form = form)

# @ROUTE DEFINTION
# NAME:     Update Account Info
# PATH:     /account
# METHOD:   GET / POST
# DESC.:    TBC
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        # TODO: Get the user info and render it into the homepage
        uid = current_user.get_id()
        if BusinessUsers.query.filter_by(bu_id = uid).first():
            return redirect(url_for('business_profile', bid = uid))
        elif IndividualUsers.query.filter_by(iu_id = uid).first():
            return redirect(url_for('individual_profile', iuid = uid))
        else:
            return render_template('500.html')
    else:
        return render_template('index.html')


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
                    ur_password_hash = hashed_password,
                    ur_phone = form.individual_contact_number.data,
                    ur_email = form.individual_email.data
                    )
        individual_user = IndividualUsers(
                                    iu_id = uid,
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
        url = url_for('request_confirmation_email', uid = user.ur_id )
        flash(Markup('{} 的個人帳號已成功註冊! 請確認電子郵件來以啟用更多功能！點擊 <a href="{}" class="alert-link">這裡</a>'.format(user.ur_login,url)), 'success')
        db.session.add(user)
        db.session.add(individual_user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('home'))
    return render_template('individual_register.html', title='註冊 - 個人帳戶', form = form)


@app.route('/individual/profile/<string:iuid>')
@login_required
def individual_profile(iuid):
    user = Users.query.get_or_404(iuid)
    profile = IndividualUsers.query.get_or_404(iuid)
    reviews = Review.query.filter_by(re_receiver_id=iuid).all()

    #create nested dictionary storing rating info of each review
    for review in reviews:
        ratings = Rating.query.filter_by(rate_re_id=review.re_id).all()
        for rating in ratings:
            review[rating.rate_rc_id] = rating
    
    return render_template('individual_profile.html', title ='我的個人檔案', user = user, profile = profile, reviews = reviews)


@app.route('/individual/profile/<string:iuid>/update', methods =['POST','GET'])
@login_required
def individual_profile_update(iuid):
    profile = IndividualUsers.query.get_or_404(iuid)
    user = Users.query.get_or_404(iuid)
    form = IndividualUpdateProfileForm()

    if form.validate_on_submit():
        #server side validation
        check_user = Users.query.filter_by(ur_phone = form.individual_contact_number.data).first()    
        if check_user and check_user.ur_id != iuid:
            flash('Contact number {} taken. Update fails.'.format(form.individual_contact_number.data), 'fail')
            return redirect(url_for('individual_profile_update', iuid = iuid))

        check_user = Users.query.filter_by(ur_email = form.individual_email.data).first()    
        if check_user and check_user.ur_id != iuid:
            flash('Email {} taken. Update fails.'.format(form.individual_email.data), 'fail')
            return redirect(url_for('individual_profile_update', iuid = iuid))
        else:
            user.ur_phone = form.individual_contact_number.data
            user.ur_email = form.individual_email.data
            profile.iu_CName = form.individual_CName.data
            profile.iu_EName = form.individual_EName.data
            profile.iu_alias = form.individual_alias.data
            profile.iu_HKID = form.individual_HKID.data
            profile.iu_selfIntroduction = form.individual_intro.data
            profile.iu_educationLevel = form.individual_educationLevel.data
            profile.iu_language_Cantonese = form.individual_language_Cantonese.data
            profile.iu_language_English = form.individual_language_English.data
            profile.iu_language_Putonghua = form.individual_language_Putonghua.data
            profile.iu_language_Other = form.individual_language_Other.data
            db.session.commit()
            flash('您的個人資料已成功更新!', 'success')
            return redirect(url_for('individual_profile_update', iuid = iuid))

    elif request.method == 'GET':	
        form.individual_contact_number.data = user.ur_phone
        form.individual_email.data = user.ur_email 
        form.individual_CName.data = profile.iu_CName
        form.individual_EName.data = profile.iu_EName 
        form.individual_alias.data = profile.iu_alias 
        form.individual_HKID.data = profile.iu_HKID 
        form.individual_intro.data = profile.iu_selfIntroduction
        form.individual_educationLevel.data = int(profile.iu_educationLevel)
        form.individual_language_Cantonese.data = profile.iu_language_Cantonese 
        form.individual_language_English.data = profile.iu_language_English 
        form.individual_language_Putonghua.data = profile.iu_language_Putonghua  
        form.individual_language_Other.data = profile.iu_language_Other 

    return render_template('individual_profile_update.html', title='更新個人資料', form = form )

@app.route('/change_password/update/<string:iuid>', methods =['POST','GET'])
@login_required
def update_password(iuid):

    user = Users.query.get_or_404(iuid)
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.ur_password_hash, form.old_password.data):
            if not bcrypt.check_password_hash(user.ur_password_hash, form.new_password.data):
                new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                user.ur_password_hash = new_hashed_password
                db.session.commit()
                flash('您的密碼已成功更新!', 'success') 
                return redirect(url_for('individual_profile_update', iuid = iuid))
            else:
                flash('Your new password cannot be same as the old one.', 'fail')
        else:
            flash('Wrong password. Please input correct old password.', 'fail')
    return render_template('update_password.html', title='update password', form = form )

# @ROUTE DEFINTION
# NAME:     View Job Board (Individual)
# PATH:     /job_board
# METHOD:   GET
# DESC.:    [GET]   The page where the individual users view listed job

@app.route('/individual/job_board', methods=['POST', 'GET'])
@login_required
def view_job_board():
    jobs = Jobs.query.all()
    return render_template('individual_job_board.html', title='工作板', jobs = jobs)

# @ROUTE DEFINTION
# NAME:     Apply Job
# PATH:     /jobs/<job_id>/apply
# METHOD:   GET
# DESC.:    [GET]   The page where the individual users view listed job

@app.route('/individual/job_board/apply/<string:job_id>', methods=['GET','POST'])
@login_required
def apply_job(job_id, list_id):

    #if the user is not current user, return 404
    if not IndividualUsers.query.filter_by(iu_id = current_user.get_id()):
        return render_template('404.html'), 404

    form = ApplyJobForm()
    
    if form.validate_on_submit():
        apid = str(uuid4())

        # Ensure the generated application ID is unique
        validate_apid = JobListings.query.filter_by(ap_id=apid).first()
        while validate_apid:
            apid = str(uuid4())
            validate_apid = Jobs.query.filter_by(jb_id=jid).first()

        application = JobApplications(
                                    ap_creationTime = datetime.utcnow(),
                                    ap_id = apid,
                                    ap_status = 'pending',
                                    ap_li_id = list_id,
                                    ap_iu_id = current_user.get_id()
                                    )
        db.session.add(application)
        db.session.commit()
        flash(f'您已成功遞交工作申請!', 'success')
        return redirect(url_for('view_job_board'))
    return render_template('individual_apply_job.html', title='申請工作',form = form,job = job_id, list = list_id)

# @ROUTE DEFINTION
# NAME:     View my jobs (individual)
# PATH:     /individual/jobs
# METHOD:   GET
# DESC.:    [GET]   The page where the individual users can view their jobs

@app.route('/individual/jobs/<string:iuid>')
@login_required
def individual_my_jobs(iuid):
    return render_template('individual_my_jobs.html',title='我的工作')

# @ROUTE DEFINTION
# NAME:     View applied jobs (individual)
# PATH:     /individual/jobs
# METHOD:   GET
# DESC.:    [GET]   The page where the individual users can view their applied jobs

@app.route('/individual/jobs/applied/<string:iuid>')
@login_required
def individual_applied_jobs(iuid):
    applications = JobApplications.query.filter_by(ap_iu_id=current_user.get_id).all()
    return render_template('individual_applied_jobs.html',title ='我的工作',applications=applications)

# @ROUTE DEFINTION
# NAME:     View enrolled jobs (individual)
# PATH:     /individual/jobs/enrolled
# METHOD:   GET
# DESC.:    [GET]   The page where the individual users can view their applied jobs

@app.route('/individual/jobs/enrolled/<string:iuid>')
@login_required
def individual_enrolled_jobs():
    applications = JobApplications.query.filter_by(ap_iu_id=current_user.get_id).all()
    enrollments = []
    for application in applications:
        nested_enrollments.append(Enrollments.query.filter_by(ap_iu_id=current_user.get_id).all())
    enrollments = lambda l: [item for sublist in l for item in sublist]
    return render_template('individual_enrolled_jobs.html',title ='我的工作',enrollments=enrollments)


@app.route('/individual/jobs/enrolled/<string:en_id>/rate',methods=['GET', 'POST'])
@login_required
def rate_n_review_on_business(en_id):
    enrollment = Enrollments.query.get_or_404(en_id)
    job_list = JobListings.query.filter_by(enrollment.en_li_id).fisrt()
    job = Jobs.query.filter_by(job_list.li_jb_id).first()
    employer = BusinessUsers.query.filter_by(job.jb_bu_id).first()

    form = RateAndReviewOnBusinessForm()
    if form.validate_on_submit():

        reid = str(uuid4())

        # Ensure the generated job listing ID is unique
        validate_reid = Jobs.query.filter_by(li_id = llid).first()
        while validate_reid:
            reid = str(uuid4())
            validate_reid = Jobs.query.filter_by(li_id = llid).first()
        
        review = Review(
                    re_id = reid,
                    re_creationTIME = datetime.utcnow(),
                    re_receiver_id = employer.bu_id,
                    re_sender_id = current_user.get_id(),
                    re_comment = form.comment.data,
                    jb_expected_paymenre_isFollowUpNeededt_days = 0,
                    re_en_id = en_id
                )
        rating_workload = Rating(
                rate_re_id = reid,
                rate_rc_id = '68469ba5-cf13-4436-a994-62376d61498e',
                rate_score = form.workload_score.data
                                )
        rating_work_environment = Rating(
                rate_re_id =  reid,
                rate_rc_id = '57169219-ca4f-4712-a6a5-6fa2fce66182',
                rate_score = form.work_environment_score.data
                                )
        rating_administration = Rating(
                rate_re_id =  reid,
                rate_rc_id = '7f0417d3-26ad-4708-ad30-d32e13d4bfba',
                rate_score = form.administration_score.data
                                )
        db.session.add(review)
        db.session.add(rating_workload)
        db.session.add(rating_work_environment)
        db.session.add(rating_administration)
        db.session.commit()

        flash(f'已成功為僱主評分!', 'success')
        #TODO: return to last page
    return render_template('rate_n_review_on_business.html', title = '僱主評分及留言', form = form)


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
                    ur_password_hash = hashed_password,
                    ur_phone = form.company_contact_number.data
                    )

        business_user = BusinessUsers(
                                    bu_id = uid,
                                    bu_address = 'NS', #not specified
                                    bu_CName = form.company_CName.data,
                                    bu_EName = form.company_EName.data,
                                    bu_picName = form.company_contact_person.data
                                    )
        db.session.add(user)
        db.session.add(business_user)
        db.session.commit()

        token = generate_confirmation_token(busniness_user.bu_email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirm_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(busniness_user.bu_email, subject, html)

        flash(f'{form.company_CName.data} 的商業帳號已成功註冊! 請確認電子郵件來以啟用帳戶！', 'success')
        return redirect(url_for('home'))
    return render_template('business_register.html', title='註冊 - 商業帳戶', form = form)

@app.route('/business/profile/<string:bid>')
def business_profile(bid):
    profile = BusinessUsers.query.get_or_404(bid)
    reviews = Review.query.filter_by(re_receiver_id=bid).all()

    #create nested dictionary storing rating info of each review
    for review in reviews:
        ratings = Rating.query.filter_by(rate_re_id=review.re_id).all()
        for rating in ratings:
            review[rating.rate_rc_id] = rating
    
    return render_template('business_profile.html',title ='我的公司檔案',profile = profile, reviews = reviews)

@app.route('/business/profile/<string:bid>/update', methods =['POST','GET'])
def business_profile_update(bid):
    profile = BusinessUsers.query.get_or_404(bid)
    user = Users.query.get_or_404(bid)
    
    form = BusinessUpdateProfileForm()
    if form.validate_on_submit():
        #TODO: add business address
        profile.bu_address = form.company_address.data
        bu_email = form.company_email.data
        if form.old_password.data and form.new_password.data and (form.old_password.data!=form.new_password.data) and (form.confirm_new_password.data == form.new_password.data):
            old_hashed_password = bcrypt.generate_password_hash(form.old_password.data).decode('utf-8')
            new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            if old_hased_password == user.ur_password_hash:
                user.ur_password_hash = new_hashed_password
                flash('您的已成功更新!', 'success')
            else:
                flash('wrong password')
        db.commit()
        flash('您的公司資料已成功更新!', 'success')
        #TODO: return to last page

    return render_template('business_profile_update.html', title='更新公司資料', form = form )

# @ROUTE DEFINTION
# NAME:     Registration (Business)
# PATH:     /business_post_job
# METHOD:   GET / POST
# DESC.:    [GET]   The page where the business user creates their account
#           [POST]  The method which validates the job info and post a job
#TODO:need to validate user type: business user
@app.route("/business/jobs/new",methods=['GET', 'POST'])
@login_required
def business_post_job():

    if not BusinessUsers.query.filter_by(bu_id = current_user.get_id()).first():
        return render_template('404.html'), 404

    form = PostJobForm()

    if not current_user.is_authenticated:
            return redirect(url_for('home'))

    if form.validate_on_submit():

        jid = str(uuid4())

        # Ensure the generated job ID is unique
        validate_jid = Jobs.query.filter_by(jb_id=jid).first()
        while validate_jid:
            jid = str(uuid4())
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
            liid = str(uuid4())
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
    if not BusinessUsers.query.filter_by(bu_id = current_user.get_id()).first():
        return render_template('404.html'), 404
    jobs = Jobs.query.filter_by(jb_bu_id = current_user.get_id()).all()
    return render_template('business_jobs_posted.html', title="已發布的工作", jobs = jobs)

# @ROUTE DEFINTION
# NAME:     View Specific Job
# PATH:     /business/jobs/<job_id>
# METHOD:   GET
# DESC.:    The page where the business user view a specific job posted
#TODO: separate specific job into business/individual view.
@app.route('/jobs/<string:job_id>')
#@login_required
def job(job_id):
s
    job = Jobs.query.get_or_404(job_id)
    listings = JobListings.query.filter_by(li_jb_id=job.jb_id).all()

    announcement_listings = []
    announcements = []
    
    for listing in listings:
        announcement_listings.append(AnnouncementListings.query.filter_by(anli_li_id = listing.li_id).all())
    for announcement_listing in announcement_listings:
        announcements.append(Announcement.query.filter_by(an_id = announcement_listing.anli_an_id).all())

    enrolled_individuals_id = []
    for listing in listings:
        enrollments = Enrollments.query.filter_by(en_li_id=listing.li_id).all()
        for enrollment in enrollments:
            application = JobApplications.query.filter_by(ap_id=enrollment.en_ap_id)
            enrolled_individuals_id.append(IndividualUsers.query.filter_by(iu_id=application.ap_iu_id).first().iu_id)
        
    #if its employer / enrolled employees, display discussion board
    if current_user.get_id() == job.jb_bu_id or (current_user.get_id() in enrolled_individuals_id):
        commentForm = CommentForm()
        if commentForm.validate_on_submit():
            
            anid = str(uuid4())

            # Ensure the generated job ID is unique
            validate_anid = Announcement.query.filter_by(an_id=anid).first()
            while validate_anid:
                anid = str(uuid4())
                validate_anid = Announcement.query.filter_by(an_id=anid).first()

            if current_user.get_id() == job.jb_bu_id:
                isFromEmployer = 1
            else:
                isFromEmployer = 0

            announcement = Announcement(
                    an_creationTime = datetime.utcnow(),
                    an_id = anid,
                    an_message = commentForm.comment.data,
                    an_sender_id = current_user.get_id(),
                    an_isFromEmployer = isFromEmployer
                    )

            for listing in listings:
                liid = str(uuid4())

                # Ensure the generated job listing ID is unique
                validate_liid = Jobs.query.filter_by(li_id = llid).first()
                while validate_liid:
                    liid = str(uuid4())
                    validate_liid = Jobs.query.filter_by(li_id = llid).first()
                announcement_listing = AnnouncementListings(
                                        anli_an_id = anid,
                                        anli_li_id = listing.li_id,
                                        anli_creationTime = datetime.utcnow()
                )
                db.session.add(announcement_listing)

            db.session.add(announcement)
            db.session.commit()

            flash(f'您的留言已成功發布!', 'success')
            return redirect(url_for('job', job_id=job_list_enrolled))

        #TODO: specific job individual user and business user validation without importing the db to html
        #TODO: listing reply under each comment using an_replyTo
        return render_template('specific_job.html',title=job.jb_title, job = job, listings = listings, commentForm = commentForm, annoucements = annoucements)

    return render_template('specific_job.html',title=job.jb_title, job = job, listings = listings, commentForm = None, annoucements = None)

@app.route('/jobs/<string:replyTo>/reply')
def reply_annoucement(an_id):
    li_id = AnnouncementListings.query.filter_by(anli_an_id=an_id).first().anli_li_id
    job_id = JobListings.query.filter_by(li_id = li_id).first().li_jb_id
    job = Jobs.query.filter_by(jb_id = job_id).first()

    commentForm = CommentForm()

    # TODO: Verify whether the indentation of the following code is correct
    if commentForm.validate_on_submit():
        
        anid = str(uuid4())

        # Ensure the generated announcement ID is unique
        validate_anid = Announcement.query.filter_by(an_id=anid).first()
        while validate_anid:
            anid = str(uuid4())
            validate_anid = Announcement.query.filter_by(an_id=anid).first()

        if current_user.get_id() == job.jb_bu_id:
            isFromEmployer = 1
        else:
            isFromEmployer = 0

        announcement = Announcement(
                an_creationTime = datetime.utcnow(),
                an_id = anid,
                an_message = commentForm.comment.data,
                an_sender_id = current_user.get_id(),
                an_isFromEmployer = isFromEmployer,
                an_replyTo = an_id
                )

        for listing in listings:
            liid = str(uuid4())

            # Ensure the generated job listing ID is unique
            validate_liid = Jobs.query.filter_by(li_id = llid).first()
            while validate_liid:
                liid = str(uuid4())
                validate_liid = Jobs.query.filter_by(li_id = llid).first()
            announcement_listing = AnnouncementListings(
                                    anli_an_id = anid,
                                    anli_li_id = listing.li_id,
                                    anli_creationTime = datetime.utcnow()
            )
            db.session.add(announcement_listing)

        db.session.add(announcement)
        db.session.commit()
        flash(f'您的回覆已成功發布!', 'success')
        
        #TODO: back to last page

    return render_template('reply_annoucement.html',title='回覆留言', an_id=an_id)

@app.route('/business/jobs/<string:job_id>/update')
def business_job_update(job_id):
    job = Jobs.query.filter_by(jb_id=job_id).first()

    #TODO: loop over lisitings
    listing = JobListings.query.filter_by(li_jb_id=job_id).first()
    
    PostJobForm = PostJobForm()
    if form.validate_on_submit():
        job.jb_description = form.job_description.data,
        job.jb_title = form.job_title.data,
        job.jb_expected_payment_days = form.job_expected_payment_days.data,
        listing.li_starttime = form.list_start_time.data,
        listing.li_endtime = form.list_end_time,
        listing.li_salary_amt = form.list_salary,
        listing.li_salary_type = form.list_salary_type,
        listing.li_quota = form.list_quota

        db.commit()
        flash(f'您的工作已成功更新!', 'success')
        
        #TODO: back to last page
    
    return render_template('job_update.html', title='更新工作',PostJobForm=PostJobForm)

@app.route('/business/jobs/<string:job_id>/delete')
def business_job_delete(job_id):
    job = job.query.get_or_404(job_id)
    if form.validate_on_submit():
        db.delete(job)
        db.commit()
        flash(f'您的工作已成功刪除!', 'success')
    return redirect(url_for('home'))

@app.route('/jobs/<string:job_id>/report/', methods =['GET','POST'])
def report_job_abnormality(job_id):
    form =  ReportAbnormalityForm()
    if form.validate_on_submit():

        abid = str(uuid4())

        # Ensure the generated job ID is unique
        validate_abid = Jobs.query.filter_by(jb_id=abid).first()
        while validate_abid:
            abid = str(uuid4())
            validate_abid = Jobs.query.filter_by(jb_id=abid).first()

        abnormality = Abnormality(
                                abn_creationTime = datetime.utcnow(),
                                abn_id = abid,
                                abn_type = 'job_abnormality',
                                abn_status = 'pending',
                                abn_jb_id = job_id,
                                abn_message = form.message.data,
                                abn_ur_id = current_user.get_id()
                                )
        db.session.add(abnormality)
        db.session.commit()

        flash(f'您的反饋已經成功傳達!', 'success')
        
        #TODO: return to last page
        
    return render_template('report_abnormality.html', title='報錯', form = form)

@app.route('/business/jobs/<string:job_id>/enrolled')
def job_list_enrolled(job_id,list_id):
    enrolled = Enrollments.query.filter_by(en_li_id=list_id).all()
    return render_template('business_job_list_enrolled.html',title="錄用中", enrolled = enrolled)

@app.route('/business/jobs/enrolled/<string:en_id>/attendance',methods=['GET', 'POST'])
def confirm_attendance(en_id):
    enrollment = Enrollments.query.get_or_404(en_id)
    form = ConfirmAttendanceForm()
    if form.validate_on_submit():
        enrollment.en_present_status = form.status.data
        db.commit()
        flash('已成功更新出席狀態','success')

        #TODO: return to last page
    
    return render_template('business_confirm_attendance.html', title='確認出席', form = form)

@app.route('/business/jobs/enrolled/<string:en_id>/rate',methods=['GET', 'POST'])
def rate_n_review_on_individual(en_id):
    enrollment = Enrollments.query.get_or_404(en_id)
    application = JobApplications.query.filter_by(enrollment.en_ap_id).first()
    listing = JobListings.query.filter_by(application.ap_li_id).first()
    job = Jobs.query.filter_by(listing.li_jb_id).first()
    job_id = job.jb_id
    employee = IndividualUsers.query.filter_by(application.ap_iu_id).first()

    form = RateAndReviewOnIndividualForm()
    if form.validate_on_submit():

        reid = str(uuid4())

        # Ensure the generated job listing ID is unique
        validate_reid = Jobs.query.filter_by(li_id = llid).first()
        while validate_reid:
            reid = str(uuid4())
            validate_reid = Jobs.query.filter_by(li_id = llid).first()
        review = Review(
                    re_id = reid,
                    re_creationTIME = datetime.utcnow(),
                    re_receiver_id = employee.iu_id,
                    re_sender_id = current_user.get_id(),
                    re_comment = form.comment.data,
                    jb_expected_paymenre_isFollowUpNeededt_days = 0,
                    re_en_id = en_id
                )
        rating = Rating(
                rate_re_id =  reid,
                rate_rc_id = 'fa4d1fcc-e870-45ee-8803-09c6dff91daf',
                rate_score = form.rating_score.data
                        )
        db.session.add(review)
        db.session.add(rating)
        db.session.commit()

        flash(f'已成功為員工評分!', 'success')
        #TODO: return to last page

    return render_template('rate_n_review_on_individual.html', title='評分及評論僱員', form = form)

# @ROUTE DEFINTION
# NAME:     View Job Applicants
# PATH:     /business/jobs/<job_id>/<sting: list_id>/applicants
# METHOD:   GET
# DESC.:    The page where the business user view list of applicant of a specific job posted
@app.route('/jobs/<string:job_id>/<string:list_id>/applications')
#@login_required
def job_list_applications(job_id, list_id):
    applicantions = JobApplications.query.filter_by(ap_li_id=list_id).all()
    listing = JobListings.query.filter_by(li_id = list_id).first()
    return render_template('business_job_list_applications.html', title='工作申請', applicantions=applications, listing = listing)

# @ROUTE DEFINTION
# NAME:     View an Job Applicant
# PATH:     /business/jobs/<job_id>/<sting: list_id>/applicants
# METHOD:   GET
# DESC.:    The page where the business user view specific job applicant of a specific job posted
@app.route('/jobs/<string:job_id>/<string:list_id>/applicants/<string:app_id>')
#@login_required
def view_an_applicant(job_id, list_id, app_id):
    applicantion = JobApplications.query.filter_by(ap_id=app_id).first()
    applicant = IndividualUsers.query.filter_by(iu_id=application.ap_iu_id).first()
    listing = JobListings.query.filter_by(li_id=application.ap_li_id).first()

    form = AcceptApplicationForm()
    
    if form.validate_on_submit():
        enid = str(uuid4())

        # Ensure the generated application ID is unique
        validate_enid = JobListings.query.filter_by(ap_id=application.ap_id).first()
        while validate_enid:
            enid = str(uuid4())
            validate_enid = Jobs.query.filter_by(jb_id=jid).first()

        enrollment = Enrollments(
                                en_creationTime = datetime.utcnow(),
                                en_id = enid,
                                en_is_paid = 0,
                                en_present_status = '',
                                en_li_id = application.ap_li_id,
                                en_ap_id = application.ap_id
                                )
        db.session.add(enrollment)
        db.session.commit()
        flash(f'工作申請已成功接受!', 'success')
        applicantions = JobApplications.query.filter_by(ap_li_id=list_id).all()
        return job_list_applications(job_id, list_id)
    
    return render_template('view_an_applicant.html',title='查看申請者',applicant=applicant,application = application,job_id = job_id,list_id = list_id)


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
