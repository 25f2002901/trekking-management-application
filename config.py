import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'this-is-a-secret-key-maybe-not-so-secret' # Used by LoginManager for session management.
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(BASE_DIR, "instance","trekverse.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Improve performance by disabling track modifications