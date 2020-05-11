from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

#Flask SQLAlchemy format
class users(db.Model):
    creationTime = db.Column(db.datetime, nullable = False, default = func.current_timestamp())
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


#SQLAlchemy format
metadata = MetaData()

users = Table('users', metadata,
    Column('ur_creationTime', TIMESTAMP, server_default = func.current_timestamp()),
    Column('ur_id', VARCHAR(1000), primary_key = True),
    Column('ur_login_name', VARCHAR(36), nullable = False),
    Column("ur_password_hash", INTEGER(36), nullable = False),
    Column("ur_isDeleted", TINYINT(1), default = 0)
)

business_users = Table('business_users', metadata,
    Column('bu_id', VARCHAR(1000), primary_key = True),
    Column('bu_address', VARCHAR(20000), nullable = False)
    Column('bu_CName', VARCHAR(36), nullable = False),
    Column('bu_EName',),
    Column('bu_picName',),
    Column('bu_phone',),
    Column('bu_isSMSVerified',),
    Column('bu_businessLogo',),
    Column('bu_isDeleted',),
    Column('bu_isBusinessVerified',)
)

individual_users = Table('individual_users', metadata,
    Column('iu_id',VARCHAR(1000), primary_key = True),
    Column('iu_phone',),
    Column('iu_isSMSVerified',),
    Column('iu_profilePicture',),
    Column('iu_isIdentityVerified',),
    Column('iu_CName',),
    Column('iu_EName',),
    Column('iu_alias',),
    Column('iu_gender',),
    Column('iu_birthday',),
    Column('iu_educationLevel',),
    Column('iu_selfIntroduction',),
    Column('iu_language_Cantonese',),
    Column('iu_language_English',),
    Column('iu_language_Putonghua',),
    Column('iu_language_Other',),
    Column('iu_isDeleted',)
)

jobs = Table('jobs', metadata,
    Column('jb_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

job_listings = Table('job_listings', metadata,
    Column('',),
)

business_address = Table('business_address', metadata,
    Column('bads_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

districts = Table('districts', metadata,
    Column('',),
)

abnormality = Table('abnormality', metadata,
    Column('abn_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

job_type = Table('job_type', metadata,
    Column('',),
)

job_applications = Table('job_applications', metadata,
    Column('ap_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

enrollments = Table('enrollments', metadata,
    Column('en_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

announcement = Table('announcement', metadata,
    Column('an_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

announcement_listings = Table('announcement_listings', metadata,
    Column('anli_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

industry = Table('industry', metadata,
    Column('',),
)

verification = Table('verification', metadata,
    Column('veri_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

rating_category = Table('rating_category', metadata,
    Column('',),
)

rating = Table('rating', metadata,
    Column('',),
)

review = Table('review', metadata,
    Column('re_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)

review_followup = Table('review_followup', metadata,
    Column('rf_creationTime', TIMESTAMP, default = func.current_timestamp()),
    Column('',),
)