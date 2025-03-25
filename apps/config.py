import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up upload folder
    UPLOAD_DIR = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'bin'}
    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default=UPLOAD_DIR)
    LOGS_FOLDER = config('LOGS_FOLDER', default=os.path.join(basedir, 'logs'))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default=os.getenv('SECRET_KEY'))

    TEMPLATES_AUTO_RELOAD = config('TEMPLATES_AUTO_RELOAD', default=True, cast=bool)

    # Config mysql
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASS')}!@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
