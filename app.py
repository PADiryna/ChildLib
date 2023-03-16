from flask import Flask, render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os, secrets
from models import Book, BookForm, UpdateBook
from PIL import Image
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    	'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
db = SQLAlchemy(app)

@app.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	books = Book.query.order_by(Book.created_at.desc()).paginate(page=page, per_page=4)
	return render_template('index.html', books=books)


@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<int:book_id>/')
def book(book_id):
	book = Book.query.get_or_404(book_id)
	return render_template('book.html', book=book) 

@app.route('/novels/')
def novels():
	page = request.args.get('page', 1, type=int)
	books = Book.query.filter(Book.genre == 'novel').paginate(page=page, per_page=4)
	return render_template('novels.html', books=books)

def save_picture(cover):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(cover.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], picture_fn)

    output_size = (220, 340)
    i = Image.open(cover)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/create/', methods=('GET', 'POST'))
def create():
    form = BookForm()
    if form.validate_on_submit():
        if form.cover.data:
            cover = save_picture(form.cover.data)
        else:
            cover ='default.jpg'   
        title = form.title.data
        author = form.author.data
        genre = form.genre.data
        description = form.description.data
        book = Book(title=title,
            author=author,
            genre=genre,
            cover=cover,
            description=description)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/<int:book_id>/edit/', methods=('GET', 'POST'))
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = UpdateBook()
    if form.validate_on_submit():
        if form.cover.data:
            cover = save_picture(form.cover.data)
        else:
            cover = book.cover
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.description = form.description.data
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred: the book already exists in the database', 'error')
            return render_template('edit.html', form=form)
      
            
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.genre.data = book.genre
        form.cover.data = book.cover
        form.description.data = book.description

    return render_template('edit.html', form=form)      

@app.post('/<int:book_id>/delete/')
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))    

@app.route('/export/')
def data():
  data = Book.query.all()
  return jsonify(data)  


if __name__ == "__main__":
  app.run(debug=True)
