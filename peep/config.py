import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

class Config:
	SECRET_KEY = config.get('DB_SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = config.get('MAIL_USER')
	MAIL_PASSWORD = config.get('MAIL_PASS')
