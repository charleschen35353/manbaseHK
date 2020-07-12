from manbase import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base(db.Model)
# Reflect the tables
engine = create_engine("mysql+pymysql://public:b05qv-x4xca@test.manbasehk.com:3306/manbasedb")

# Inherit UserMixin Property and redefine get_id due to different id name
class Users(Base, UserMixin):
    __table_name__ = 'users'
    def get_id(self):
        return str(self.ur_id)
        

Base.prepare(engine, reflect=True)

# Mapped classes are now created with names by default
# matching that of the table name.
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
