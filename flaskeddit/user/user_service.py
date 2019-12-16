from flaskeddit.models import AppUser


def get_user(username):
    """
    Gets a user by name from the database.
    """
    user = AppUser.query.filter_by(username=username).first()
    return user

def get_email(email):
    """
    Gets a user by name from the database.
    """
    email = AppUser.query.filter_by(email=email).first()
    return email
