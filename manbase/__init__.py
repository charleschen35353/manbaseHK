from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets
from flask.ext.uuid import FlaskUUID

csrf = CSRFProtect()

app = Flask(__name__)
FlaskUUID(app)
uri = 'sqlite:///site.db'
#uri = 'mysql://public:b05qv-x4xca@localhost/manbasedb'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from manbase import routes
