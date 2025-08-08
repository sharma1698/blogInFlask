# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
