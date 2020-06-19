from manbase import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

Base = automap_base(db.Model)
# reflect the tables
engine = create_engine("mysql+mysqldb://lancetpk:lancetpk@test.manbasehk.com:3306/manbasedb")

#inherit UserMixin Property and redefine get_id due to different id name
class Users(Base, UserMixin):
    __table_name__ = 'users'
    def get_id(self):
        return (self.ur_id)

Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
#Users = Base.classes.users
BusinessUsers = Base.classes.business_users
IndividualUsers = Base.classes.individual_users
Jobs = Base.classes.jobs
JobListings = Base.classes.job_listings
BusinessAddress = Base.classes.business_address
Districts = Base.classes.districts
Abnormality = Base.classes.abnormality
JobType = Base.classes.job_type
JobApplications  = Base.classes.job_applications
Enrollments = Base.classes.enrollments
Announcement = Base.classes.announcement
AnnouncementListings = Base.classes.announcement_listings
Industry = Base.classes.industry
Verification = Base.classes.verification
RatingCategory = Base.classes.rating_category
Rating = Base.classes.rating
Review = Base.classes.review
ReviewFollowup = Base.classes.review_followup

session = Session(engine)

'''
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default = "default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_on':type
    }

    def __repr__(self):
        return "User(\'{}\',\'{}\',\'{}\')".format(self.username, self.email, self.profile_image)

class User(db.Model):
    __table_name__= "individual_users" 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(8), primary_key=True)
    sms_verified = db.Column(db.Boolean, primary_key=True)
    # long list of attributes TODO
    
    def __repr__(self):
        return "User(\'{}\',\'{}\',\'{}\')".format(self.username, self.email, self.image_file)
        
class Post(db.Model):
    __table_name__= "posts" 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , nullable=False)

    def __repr__(self):
        return "Post(\'{}\',\'{}\')".format(self.title, self.date_posted)
'''