from flask import flash, redirect, render_template, request, url_for, session, abort
from flask_login import current_user, login_required
from flaskeddit.models import *
from io import BytesIO
from flaskeddit import *
from flask_mail import Mail,Message
from flask import current_app

from flaskeddit.auth import auth_blueprint, auth_service
from flaskeddit.auth.forms import LoginForm, RegisterForm
from flaskeddit import mail
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, EqualTo

import qrcode
import qrcode.image.svg as svg

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for registering new users. On a GET request, it returns the registration
    form. On a POST request, it handles user registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
            
    form = RegisterForm()
    if form.validate_on_submit():
        auth_service.register_user(form.username.data, form.email.data,form.password.data)
        flash("Successfully registered.", "primary")
        session['username'] = form.username.data
        #send_mail(form.email.data)
        return redirect(url_for('auth.tfa'))
    return render_template("register.html", form=form)



@auth_blueprint.route("/tfa")
def tfa():
    if 'reg_username' in session:
        return redirect(url_for('feed.feed'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return render_template('tfa.html'), headers

@auth_blueprint.route("/qr_code")
def qr_code():
    if 'username' not in session:
        return redirect(url_for('feed.feed'))
    
    user = AppUser.query.filter_by(username=session['username']).first()
    session.pop('username')
    img = qrcode.make(user.get_auth_uri(), image_factory=svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)
    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return stream.getvalue(), headers


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for logging in users. On a GET request, it returns the login form. On a POST
    request, it handles user login.
    """
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
    form = LoginForm()
    if form.validate_on_submit():
        login_successful = auth_service.log_in_user(
            form.username.data, form.password.data)
        if login_successful:
            flash("Successfully logged in.", "primary")
            next_location = request.args.get("next")
            if next_location is None or not next_location.startswith("/"):
                next_location = url_for("feed.feed")
            return redirect(next_location)
        else:
            flash("Login Failed", "danger")
            return redirect(url_for("auth.login"))
    return render_template("login.html", form=form)


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Route for logging out current users.
    """
    auth_service.log_out_user()
    flash("Successfully logged out.", "primary")
    return redirect(url_for("auth.login"))
