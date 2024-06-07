from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .models import Book, Style, Cover
import os, hashlib
from . import db

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home_page():
    books = Book.query.order_by(Book.year.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = books.paginate(page=page, per_page=10)

    return render_template("home.html", user=current_user, books=books, pages=pages)

@views.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        style = request.form.getlist('style')
        short_description = request.form.get('short_description')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        pages = request.form.get('pages')

        if not all([title, style, year, publisher, author, pages, short_description != 'Краткое описание']):
            flash("Пожалуйста, введите все данные", category="error")
        else:
            if 'file' not in request.files:
                flash("Пожалуйста, введите все данные", category="error")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash("Пожалуйста, введите все данные", category="error")
                return redirect(request.url)
            if file and allowed_file(file.filename):   
                file_md5 = hashlib.md5(file.read()).hexdigest() 
                filename = secure_filename(file.filename)
                try:
                    cover = Cover.query.filter_by(MD5_hash=file_md5).first()
                    if cover:
                        cover_id = cover.id
                    else:
                        new_cover = Cover(file_name=filename, MIME_type=file.content_type, MD5_hash=file_md5)
                        db.session.add(new_cover)
                        db.session.flush() 
                        cover_id = new_cover.id
                    new_book = Book(title=title, short_description=short_description, year=year, publisher=publisher, author=author, pages=pages, cover_id=cover_id)
                    styles = Style.query.filter(Style.id.in_(style)).all()
                    new_book.styles.extend(styles)
                    db.session.add(new_book)
                    db.session.commit()
                    file.seek(0)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    flash("При сохранении данных возникла ошибка. Проверьте корректность введённых данных.", category="error")                  

    styles = Style.query.all()
    return render_template("add_book.html", user=current_user, book=None, styles=styles)