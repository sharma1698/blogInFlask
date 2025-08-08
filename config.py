# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))
local_server = True
class Config:
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if local_server:
        SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_blog'
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql://user:password@prod-server/flask_blog'
    FB_URL = 'https://www.facebook.com/'
    TW_URL = 'https://x.com/i/flow/login'
    GT_URL = 'https://github.com'
