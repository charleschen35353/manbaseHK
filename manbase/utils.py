from manbase import app, mail, db
from manbase.models import *
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import secrets

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def generate_confirmation_token_for(user, purpose):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    key = secrets.token_hex(16)
    if purpose == "reset":
        user.ur_reset_key = key
    elif purpose == "email":
        user.ur_email_key = key
    elif purpose == "SMS":
        user.ur_SMS_key = key
    else:
        raise
    db.session.commit()
    return serializer.dumps(user.ur_email + key, salt=app.config['SECURITY_PASSWORD_SALT'])

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
        elif purpose == "SMS" and user.ur_SMS_key == key: return email 
        else:
            raise
    except:
        raise

    return email
