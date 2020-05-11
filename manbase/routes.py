from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user , current_user
from manbase import app, db, bcrypt
from manbase.forms import RegistrationForm, LoginForm
from manbase.models import User, Post


posts = [ #fake db return
	{
		'author': "Charles Chen",
		'title': "Home Page Prototype",
        	'content': "This is the home page of ManBase",
       		'date_posted': "May 6, 2020",
	} 
]

db.create_all()
isLogin = False
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title = "about us")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {}. You are able to log in. ".format(form.username.data),"success")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, isLogin=isLogin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         if user and bcrypt.check_password_hash(user.password, form.password.data):
             login_user(user, remember = form.remember.data)
             isLogin = True
             flash("Login Successful.".format(form.email.data),"success")
             return redirect(url_for('home'))
         else:
             flash('Login Failed. Please check email or password', 'fail')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'sucess')
    return redirect(url_for('home'))


@app.route('/account')
def account():
    return render_template('account.html', title='account')


