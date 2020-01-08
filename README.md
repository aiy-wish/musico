# [Musico](https://musico-flask-app.herokuapp.com)
A user friendly, secured flask app for music enthusiasts where one can browse through different musico pages and post anything and reply to anything 

## Features
- Secure Registration and authentication
  -2FA with QR Code and giving token number every time a user is logging in.
- Ability to create communities
- Ability to post and reply to posts in the communities
-	Edit or delete your communities, posts and replies
-	Follow communities and get posts on your feed page
-	Upvote or downvote posts and replies
-	Sort communities, posts and replies by latest or most popular
-	View user profiles and view posts

## Functionality
- Login and Registration Page (All under flaskeddit/auth/routes.py and forms.py)
  -Passwords are hashed and are double checked
  -Then it goes to the 2FA page where the user scans the QR code and then gets a token which expires and regenerates after 30 seconds
    which is then used for logging in.
- Feed  (All under flaskeddit/feed/routes.py , forms.py, communities/routes.py, forms.py)
  - The feed can be classified as new or top posts (depending on time and total votes respectively).
  - One can visit any musico groups where the user can post or reply to any post. Ability to upvote or downvote a post.
  - One can make and join musico groups related to music. If not related to music then it will be deleted by the admin.
  - Ability to check each user’s profile page.
  - One can edit their post or reply easily by clicking on edit.
  - The description of the musico page can also be changed

## Forms
- User Management: Login and Registration Pages
- Functionality: Post Feed, Reply, Create Community, Edit anything.

## Security
- Proper CSP 
- CSRF-protected forms
- Talisman Protected
- Passwords are Hashed
- 2 factor Authentication with Duo (Mandatory for every user whenever they login)

## Python Packages used
- Python
- Flask
- Flask-Talisman
- Flask-SQLAlchemy
- Flask-WTForms
- Flask-Login
- Flask-Bcrypt
- Flask_Mail
- QRCode
- SQLite

## Testing

Musico is tested using pytest.

Use `pytest` to run the application's tests.

```
pytest
```

## Deployment

Musico is automatically deployed to [Heroku](https://www.heroku.com/) using [CircleCI](https://circleci.com/).

You can also use `git` to manually deploy the application.

```
export HEROKU_API_KEY="heroku_api_key"
export HEROKU_APP_NAME="heroku_app_name"
git push https://heroku:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git master
```

## Built With

* [Flask](http://flask.pocoo.org/) - Python Framework
* [Bootstrap](https://getbootstrap.com/) - CSS Framework


## Acknowledgments

* [favicon.io](https://favicon.io/) - For the matching favicon.
* [logohub.io](https://logohub.io/) - For the neat logo.
* [reddit](https://www.reddit.com/) - The inspiration for this site.



