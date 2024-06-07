from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32), nullable=False, unique=True)
    description = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    users = db.relationship('User', backref='role')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.VARCHAR(16), unique=True, nullable=False)
    password_hash = db.Column(db.VARCHAR(1000), nullable=False)
    last_name = db.Column(db.VARCHAR(64), nullable=False)
    first_name = db.Column(db.VARCHAR(64), nullable=False)
    middle_name = db.Column(db.VARCHAR(64))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    reviews = db.relationship('Review', backref='users')

book_style = db.Table("book_style", 
     db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
     db.Column('style.id', db.Integer, db.ForeignKey('style.id')))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(200), unique=True, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    publisher = db.Column(db.VARCHAR(64), nullable=False)
    author = db.Column(db.VARCHAR(64), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'))
    styles = db.relationship('Style', secondary='book_style', backref='books')
    reviews = db.relationship('Review', backref='books')

class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style_name = db.Column(db.VARCHAR(200), nullable=False, unique=True)

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.VARCHAR(200), nullable=False)
    MIME_type = db.Column(db.VARCHAR(200), nullable=False)
    MD5_hash = db.Column(db.VARCHAR(200), nullable=False)
    books = db.relationship('Book', backref='cover')

class Review(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, default=func.now())
