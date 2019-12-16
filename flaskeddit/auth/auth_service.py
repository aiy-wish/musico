from flask_login import login_user, logout_user
from passlib.hash import bcrypt
from flask_mail import Mail,Message
from flaskeddit import mail
from flaskeddit import db
from flaskeddit.models import AppUser


def register_user(username, email, password):
    """
    Hashes the given password and registers a new user in the database.
    """
    hashed_password = bcrypt.hash(password)
    app_user = AppUser(username=username.lower(), email = email.lower(), password=hashed_password)
    db.session.add(app_user)
    db.session.commit()


def log_in_user(username, password):
    """
    Hashes and compares the given password with the stored password. If it is a match,
    logs a user in.
    """
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    if app_user and bcrypt.verify(password, app_user.password):
        login_user(app_user)
        return True
    else:
        return False


def log_out_user():
    """
    Logs the current user out.
    """
    logout_user()

def send_mail(email):
	try:
		msg = Message("Send Mail Tutorial!",
		  sender="boiflask@gmail.com",
		  recipients=email)
		msg.body = "Yo!\nHave you heard the good word of Python???"           
		mail.send(msg)
		return 'Mail sent!'
	except Exception as e:
		return(str(e)) 