from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

from flaskeddit.config import Config
from flask_talisman import Talisman


db = SQLAlchemy()
bcrypt = Bcrypt()
talisman = Talisman()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"

csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'media-src' : ['*'],
    'script-src': ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css', 'https://use.fontawesome.com/releases/v5.8.1/css/all.css','https://code.jquery.com/jquery-3.3.1.slim.min.js','https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js', 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js'],
} 
mail = None

def create_app(config=Config):

    """
    Factory method for creating the Flaskeddit Flask app.
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'boiflask@gmail.com',
        MAIL_PASSWORD = 'Flaskboi@2019'
    )
    mail = Mail(app)


    
    app.config["SECRET_KEY"] = b'\t\xbbQ\xce\xb7:P\xc6w\x84\xae)98Mu\xa2\xfe1\x9c \x0b\xff\xdf'
    #talisman.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from flaskeddit.auth import auth_blueprint
    from flaskeddit.communities import communities_blueprint
    from flaskeddit.community import community_blueprint
    from flaskeddit.feed import feed_blueprint
    from flaskeddit.post import post_blueprint
    from flaskeddit.reply import reply_blueprint
    from flaskeddit.user import user_blueprint
    from flaskeddit.cli import cli_app_group

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(communities_blueprint)
    app.register_blueprint(community_blueprint)
    app.register_blueprint(feed_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(reply_blueprint)
    app.register_blueprint(user_blueprint)
    app.cli.add_command(cli_app_group)

    #talisman.content_security_policy = csp
    #talisman.content_security_policy_report_uri = "/csp_error_handling"


    return app

