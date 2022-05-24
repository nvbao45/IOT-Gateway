import os
from decouple import config


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up upload folder
    UPLOAD_DIR = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'bin'}
    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default=UPLOAD_DIR)
    LOGS_FOLDER = config('LOGS_FOLDER', default=os.path.join(basedir, 'logs'))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    TEMPLATES_AUTO_RELOAD = config('TEMPLATES_AUTO_RELOAD', default=True, cast=bool)

    # Config mysql
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://baonv:BaoNV040597!@192.168.31.246/UiTiOt'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://baonv:BaoNV040597!@localhost/UiTiOt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config mail server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'nvbao4566@gmail.com'
    MAIL_PASSWORD = 'BaoNV040597!'
    MAIL_DEFAULT_SENDER = '"UiTiOt" <noreply@gateway.com>'

    # Config Flask-User
    USER_APP_NAME = 'UiTiOt'
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = 'noreply@example.com'


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgresSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='appseed'),
        config('DB_PASS', default='pass'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='UiTiOt')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
