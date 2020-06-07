from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

app = Flask(__name__)

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://public:b05qv-x4xca@localhost/manbasedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.Model = automap_base(db.Model)

@app.route('/')
def hello_world():
    return 'Hello, World!'


