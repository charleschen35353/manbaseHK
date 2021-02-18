import secrets
import nexmo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uuid import FlaskUUID
# TODO: Add support for flask_assets for JS Bundling
# TODO: Add support for flask_minify for HTML and CSS Minifying
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail

csrf = CSRFProtect()

app = Flask(__name__)

# TODO: Convert the URI and SECRET_KEY into Environment Variables
#       Use 'localhost' instead for deployment
uri = 'mysql+pymysql://public:b05qv-x4xca@manbasehk.org:3306/manbasedb'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['KEY_LENGTH'] = len(app.config['SECRET_KEY'])
app.config['SECURITY_PASSWORD_SALT'] = 'P@ssWoRdSaltManb@seHK'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'manbasehk@gmail.com'
app.config['MAIL_PASSWORD'] = 'manbasehk2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'manbasehk@gmail.com' 
# Using default error message translation
app.config['WTF_I18N_ENABLED'] = False
app.config['DEFAULT_STRING'] = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%'
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LftibMZAAAAAETVT1059c9ue_KF7Ftbt7LSl7rW'
app.config['RECAPTCHA_PRIVATE_KEY']='6LftibMZAAAAAGmClcZ6jgqhmGl-2Pceuo8OZVBs'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
app.config['SMS_PROVIDER'] = nexmo.Client(key='e23983df', secret='5u0gzHpvJgKnNpJ1')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
uuid = FlaskUUID(app)
login_manager = LoginManager(app)
mail = Mail(app)
from manbase import routes
