from manbase import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default = "default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
        
    '''
    __mapper_args__ = {
        'polymorphic_on':type
    }
    '''
    def __repr__(self):
        return "User(\'{}\',\'{}\',\'{}\')".format(self.username, self.email, self.profile_image)

'''
class Individual_User(db.Model):
    __table_name__= "individual_users" 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(8), primary_key=True)
    sms_verified = db.Column(db.Boolean, primary_key=True)
    # long list of attributes TODO
    def __repr__(self):
        return "User(\'{}\',\'{}\',\'{}\')".format(self.username, self.email, self.image_file)
'''

class Post(db.Model):
    __table_name__= "posts" 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , nullable=False)

    def __repr__(self):
        return "Post(\'{}\',\'{}\')".format(self.title, self.date_posted)
