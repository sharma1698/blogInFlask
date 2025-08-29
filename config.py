# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))
local_server = True
class Config:
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    db_host = os.getenv("DB_HOST", "localhost")  # defaults to localhost if not set
    if local_server:
         SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:root@db:3306/flask_blog"  #using docker
        # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_blog'   # without docker
        # SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:root@{db_host}:3306/flask_blog"
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql://user:password@prod-server/flask_blog'
    FB_URL = 'https://www.facebook.com/'
    TW_URL = 'https://x.com/i/flow/login'
    GT_URL = 'https://github.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'techcheer1698@gmail.com'   # Your Gmail address
    MAIL_PASSWORD = 'nfkpohordrnfnveq'    # Use an App Password for Gmail
    MAIL_DEFAULT_SENDER = ('My Blog', 'techcheer1698@gmail.com')
    ADMIN_USERNAME ='shweta'
    ADMIN_PASSWORD ='Shweta123'
    UPLOAD_FOLDER = 'static/uploads'