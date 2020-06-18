import secrets
import os
import cv2
import matplotlib.image as pltimg
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user , current_user, login_required
from manbase import app, db, bcrypt,uuid
from manbase.forms import BusinessRegistrationForm,RegistrationForm, LoginForm, UpdateAccountForm
from manbase.models import Users, BusinessUsers
from datetime import datetime

posts = [ #fake db return
	{
		'author': "Charles Chen",
		'title': "Home Page Prototype",
        	'content': "This is the home page of ManBase",
       		'date_posted': "May 6, 2020",
	} 
]

isLogin = False
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', posts=posts)
    else:
        return render_template('index.html')
    

'''suspend'''
# TODO: Incorporate this template as the landing page
# This should replace the '/' route
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title = "about us")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        '''hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()'''
        flash("Account created for {}. You are able to log in. ".format(form.username.data),"success")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, isLogin=isLogin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        if login == 'test' and password == 'testing':
            flash("成功登入.".format(form.login.data),"success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('登入失敗. 請重新檢查帳號或密碼.', 'fail')

        '''user = User.query.filter_by(login=form.login.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            isLogin = True
            flash("成功登入.".format(form.login.data),"success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('登入失敗. 請重新檢查帳號或密碼.', 'fail')'''
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('您已成功登出.', 'success')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    img = pltimg.imread(form_picture)
    img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(picture_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    #form_picture.save(picture_path)
    return picture_fn

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
        '''db.session.commit()'''
        flash("Account Info Updated")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.profile_image)
    return render_template('account.html', title='account', image_file = image_file, form = form)
'''end suspend'''


'''business'''
@app.route("/business_register",methods=['GET', 'POST'])
def business_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = BusinessRegistrationForm()
    if form.validate_on_submit():
        '''hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        uid = uuid.uuid4()

        #ensure unique uid
        validate_uid = Users.query.filter_by(ur_id=uid).first()
        while validate_uid:
            uid = uuid.uuid4()
            validate_uid = Users.query.filter_by(ur_id=uid).first()

        user = Users(
                    ur_creationTime = datetime.now, 
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
        '''
        flash(f'{form.company_CName.data} 的商業帳號已成功註冊!', 'success')
        return redirect(url_for('business_register_confirm'))
    return render_template('business_register.html', title='註冊 - 商業帳戶', form = form)

@app.route('/business_register_confirm', methods=['GET','POST'])
def business_register_confirm():
    return render_template('business_register_confirm.html',title = '註冊 - 商業帳戶資料確認')


# Error Handler

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500