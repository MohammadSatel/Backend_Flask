# views.py
from flask import Blueprint, request, jsonify
from project import db
from project.books.models import Book

# Blueprint for books API
books_api = Blueprint('books_api', __name__, url_prefix='/api/books')

# Route to fetch books in JSON format
@books_api.route('/', methods=['GET'])
def list_books():
    books = Book.query.all()
    book_list = [
        {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'book_type': book.book_type,
            'status': book.status
        } for book in books
    ]
    return jsonify(books=book_list)

# Route to create a new book
@books_api.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        name=data['name'],
        author=data['author'],
        year_published=data['year_published'],
        book_type=data['book_type']
    )
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating book: {str(e)}'}), 500
    
# Route to update an existing book
@books_api.route('/<int:book_id>/', methods=['PUT'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    data = request.get_json()
    book.name = data.get('name', book.name)
    book.author = data.get('author', book.author)
    book.year_published = data.get('year_published', book.year_published)
    book.book_type = data.get('book_type', book.book_type)
    try:
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating book: {str(e)}'}), 500

# Route to delete a book
@books_api.route('/<int:book_id>/', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting book: {str(e)}'}), 500

# Route to get book details
@books_api.route('/<int:book_id>/', methods=['GET'])
def get_book_details(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    book_data = {
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'year_published': book.year_published,
        'book_type': book.book_type,
        'status': book.status
    }
    return jsonify(book=book_data)