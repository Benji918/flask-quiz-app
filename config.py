import os

# from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'

    # # mail settings
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    #
    # # gmail authentication
    # MAIL_USERNAME = 'kodiugos@gmail.com'
    # MAIL_PASSWORD = 'llhytkakbfhnikci'
    #
    # # mail accounts
    # MAIL_DEFAULT_SENDER = 'kodiugos@gmail.com'

