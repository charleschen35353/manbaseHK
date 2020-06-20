from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets
from flask_uuid import FlaskUUID

csrf = CSRFProtect()

app = Flask(__name__)
uri = 'mysql+mysqldb://public:b05qv-x4xca@test.manbasehk.com:3306/manbasedb'
#uri = 'mysql://public:b05qv-x4xca@localhost/manbasedb'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#using default error message translation
app.config['WTF_I18N_ENABLED'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
uuid = FlaskUUID(app)
login_manager = LoginManager(app)

from manbase import routes
