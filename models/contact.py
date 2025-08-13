from . import db  #The . means current package ,db refers to a variable or object defined in that package
from sqlalchemy.sql import func

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)  # if have primary key then default it take auto increment
    name = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.BigInteger, nullable=False)
    msg = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
     # server_default: Tells SQL to automatically insert the current timestamp.
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())