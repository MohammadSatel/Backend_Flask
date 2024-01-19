from flask import Blueprint, request, jsonify
from project import db
from project.loans.models import Loan
from project.books.models import Book
from project.customers.models import Customer

# Blueprint for loans API
loans_api = Blueprint('loans_api', __name__, url_prefix='/api/loans')

# Route to list all loans
@loans_api.route('/', methods=['GET'])
def list_loans():
    loans = Loan.query.all()
    loan_list = [
        {
            'id': loan.id,
            'customer_name': loan.customer_name,
            'book_name': loan.book_name,
            'loan_date': loan.loan_date.isoformat(),
            'return_date': loan.return_date.isoformat()
        } for loan in loans
    ]
    return jsonify(loans=loan_list)

# Route to create a new loan
@loans_api.route('/', methods=['POST'])
def create_loan():
    data = request.get_json()
    book = Book.query.filter_by(name=data['book_name'], status='available').first()
    if not book:
        return jsonify({'error': 'Book not available for loan.'}), 400

    try:
        new_loan = Loan(
            customer_name=data['customer_name'],
            book_name=data['book_name'],
            loan_date=data['loan_date'],
            return_date=data['return_date'],
            original_author=book.author,
            original_year_published=book.year_published,
            original_book_type=book.book_type
        )
        db.session.add(new_loan)
        db.session.delete(book)  # This line removes the book from available books
        db.session.commit()
        return jsonify(new_loan.id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating loan: {str(e)}'}), 500

# Route to delete a loan
@loans_api.route('/<int:loan_id>/', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    try:
        book = Book(
            name=loan.book_name,
            author=loan.original_author,
            year_published=loan.original_year_published,
            book_type=loan.original_book_type,
            status='available'  
        )
        db.session.add(book)  # This line adds the book back to available books
        db.session.delete(loan)
        db.session.commit()
        return jsonify({'message': 'Loan deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting loan: {str(e)}'}), 500

# Route to get loan details
@loans_api.route('/<int:loan_id>/', methods=['GET'])
def get_loan_details(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    loan_data = {
        'id': loan.id,
        'customer_name': loan.customer_name,
        'book_name': loan.book_name,
        'loan_date': loan.loan_date.isoformat(),
        'return_date': loan.return_date.isoformat()
    }
    return jsonify(loan=loan_data)