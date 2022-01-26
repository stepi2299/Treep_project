import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'key-our')
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_PORT = os.environ.get("DB_PORT", 5432)
    DB_NAME = os.environ.get("DB_NAME", "treep_practice")
    DB_HOST = os.environ.get("DB_NAME", "localhost")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, "app", "static", "photos")
