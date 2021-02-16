from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from peep.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # same value we'd use w/ url_for
login_manager.login_message_category = 'info' # bootstrap class
mail = Mail()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# fetch and register blueprints
	from peep.users.routes import users
	from peep.posts.routes import posts
	from peep.main.routes import main
	from peep.errors.handlers import errors
	from peep.images.routes import images
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	app.register_blueprint(images)

	return app