from . import db  #The . means current package ,db refers to a variable or object defined in that package
from sqlalchemy.sql import func

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)  # if have primary key then default it take auto increment
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(20), unique=True,nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    img_file = db.Column(db.String(50),nullable=False)
    tag_line = db.Column(db.String(50),nullable=False)
    deleted_at = db.Column(db.DateTime , nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())