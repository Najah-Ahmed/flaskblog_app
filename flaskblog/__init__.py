
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' 


db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'

 
mail=Mail()


#import route




def create_app(config_class=Config):
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'najahsaid'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sites.db'
	app.config.from_object(Config)
	from flaskblog.users.routes import users
	from flaskblog.main.routes import main
	from flaskblog.posts.routes import posts
	from flaskblog.errors.handler import errors
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	app.register_blueprint(users)
	app.register_blueprint(main)
	app.register_blueprint(posts)
	app.register_blueprint(errors)

	
	return app
