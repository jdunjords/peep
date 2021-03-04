import os

class Config:
	SECRET_KEY = '11111111121212'#'#os.environ.get('DB_SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USER')
	MAIL_PASSWORD = os.environ.get('MAIL_PASS')
