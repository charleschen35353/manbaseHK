import secrets
import math
import random
import cv2
import matplotlib.image as pltimg
import os
from manbase import *
from manbase.models import *
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

def save_picture(form_picture):
    """
    A utility function which helps save the profile picture in 'static/profile_pics',
    and return the new name of the profile picture
    """
    # Rename the profile picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the picture and save it in the path
    img = pltimg.imread(form_picture)
    img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(picture_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return picture_fn
    
def send_SMS(to, message):
    app.config['SMS_PROVIDER'].send_message({
        'from': 'ManbaseHK',
        'to': to,
        'text': message + '\n',
    })
    app.logger.info('SMS sent to {}'.format(to))

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    app.logger.info('Email sent to {}'.format(to))

def generate_confirmation_token_for(user, purpose):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    key = secrets.token_hex(16)
    if purpose == "reset":
        user.ur_reset_key = key
    elif purpose == "email":
        user.ur_email_key = key
    else:
        raise
    db.session.commit()
    app.logger.info('token generate for {} purpose. user: {}'.format(purpose, user.ur_id))
    return serializer.dumps(user.ur_email + key, salt=app.config['SECURITY_PASSWORD_SALT'])

def generate_otp_for(user):
    otp = ""
    length = len(app.config['DEFAULT_STRING']) 
    for i in range(6) : 
        otp += app.config['DEFAULT_STRING'] [math.floor(random.random() * length)] 
        
    user.ur_otp_hash = bcrypt.generate_password_hash(otp).decode('utf-8')
    db.session.commit()
    app.logger.info('otp generated for user {}'.format(user.ur_id))
    return otp

def confirm_token_for(token, purpose ,expiration=18000): 
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email_concatenated = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )

        key = email_concatenated[len(email_concatenated) - app.config['KEY_LENGTH']:len(email_concatenated)]
        email = email_concatenated[:len(email_concatenated) - app.config['KEY_LENGTH']]
        user = Users.query.filter_by(ur_email = email).first()
        if purpose == "reset" and user.ur_reset_key == key: return email
        elif purpose == "email" and user.ur_email_key == key: return email
        else:
            raise
    except:
        raise
    app.logger.info('Email token confirmed for {} purpose. user: {}'.format(purpose, user.ur_id))
    return email
