from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError
from models import Book


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