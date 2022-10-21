import os 
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
	SECRET_KEY = os.getenv('SECRET_KEY') or 'default-flask-key'
	FLASK_APP = os.getenv('FLASK_APP') or 'application.py'
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	@classmethod
	def print(cls):
		print(cls.SECRET_KEY, cls.SQLALCHEMY_DATABASE_URI, cls.FLASK_APP, cls.SQLALCHEMY_TRACK_MODIFICATIONS)
