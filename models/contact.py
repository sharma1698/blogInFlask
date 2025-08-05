from models import db
import datetime

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)  # if have primary key then default it take auto increment
    name = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False,server_default=datetime.datetime.now())  # server_default: Tells SQL to automatically insert the current timestamp.
    email = db.Column(db.String(120), nullable=False)
