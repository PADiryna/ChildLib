from flask_sqlalchemy import SQLAlchemy
from . import db
# from app import db
# from sqlalchemy.sql import func
# import sqlalchemy as db
# from sqlalchemy import create_engine, Table, Column, Integer, MetaData
import json
from dataclasses import dataclass
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError



@dataclass
class Book(db.Model):
    id: int
    title: str
    author: str
    genre: str
    cover: str
    description: str

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	author = db.Column(db.String(100), nullable=False)
	genre = db.Column(db.String(20), nullable=False)
	cover = db.Column(db.String(50), nullable=False, default='default.jpg')
	description = db.Column(db.Text)

	def __repr__(self):
            return f'<Book {self.title}>'	
        
db.create_all()
        
# engine = db.create_engine('sqlite:///database.db')

# connection = engine.connect()

# metadata = db.MetaData()

# Book = db.Table('stations', metadata,
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('titile', db.String(100)), 
#     db.Column('author', db.String(100)), 
#     db.Column('genre', db.String(20)), 
#     db.Column('cover', db.String, default='default.jpg'), 
#     db.Column('description', db.Text) 
# )

# metadata.create_all(engine)

# insert_query = Book.insert()


with open('books.json', encoding="utf8") as f:
	books_json = json.load(f)
	for book in books_json:
		book = Book(title=book['title'], 
	      author=book['author'],
	      genre=book['genre'],  
	      description=book['description']
)
		db.session.add(book)
		db.session.commit()		

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=5, max=100)])
    author = StringField('Author', validators=[DataRequired(),Length(min=5, max=100)])
    genre = StringField('Genre', validators=[DataRequired(),Length(min=5, max=20)])
    cover = FileField('Cover', validators=[FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description',validators=[DataRequired(),Length(max=500)])
    submit = SubmitField('Add')

    def validate_title(self, title):
        title = Book.query.filter_by(title=title.data).first()
        if title:
            raise ValidationError('This book is already on my reading list.')


class UpdateBook(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=5, max=100)])
    author = StringField('Author', validators=[DataRequired(),Length(min=5, max=100)])
    genre = StringField('Genre', validators=[DataRequired(),Length(min=5, max=20)])
    cover = FileField('Cover', validators=[FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Deskription',validators=[DataRequired(),Length(max=500)])
    submit = SubmitField('Update')	


book = Book()


