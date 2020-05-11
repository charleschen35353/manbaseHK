from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

app = Flask(__name__)

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://public:b05qv-x4xca@localhost/manbasedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

class users(db.Model):
    creationTime = db.Column(db.datetime, nullable = False, default = func.current_timestamp()
    id = db.Column(db.String(1000), primary_key = True)
    login_name = db.Column(db.String(36), nullalbe = False)

class business_users(db.Model):
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class individual_users(db.Model):
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class jobs(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class job_listings(db.Model):
    id = db.Column(db.String(1000), primary_key = True)

class business_address(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class districts(db.Model):
    id = db.Column(db.String(1000), primary_key = True)

class abnormality(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class job_type(db.Model):
    id = db.Column(db.String(1000), primary_key = True)

class job_applications(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class enrollments(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class announcement(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class announcement_listings(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class verification(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class rating_category(db.Model):
    id = db.Column(db.String(1000), primary_key = True)

class rating(db.Model):
    id = db.Column(db.String(1000), primary_key = True)

class review(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

class review_followup(db.Model):
    creationTime = db.Column(db.datetime(timezone = ture), nullable = False, server_default = func.current_timestamp())
    id = db.Column(db.String(1000), primary_key = True)
    columnName = db.Column(db.type, )

#TEMPLATE
# class name(db.Model):
# columnName = db.Column(db.type, )
