import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-flask-key'
    FLASK_APP = os.environ.get('FLASK_APP') or 'application.py'