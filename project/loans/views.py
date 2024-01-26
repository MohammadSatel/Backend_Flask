from flask import Blueprint, request, jsonify, make_response
from project import db
from project.loans.models import Loan
from project.books.models import Book
from project.customers.models import Customer
from flask_cors import CORS

# Blueprint for loans API with CORS enabled
loans_api = Blueprint('loans_api', __name__, url_prefix='/api/loans')
CORS(loans_api)

# Route to list all loans
@loans_api.route('/', methods=['GET'])
def list_loans():
    # Query all loans from the database
    loans = Loan.query.all()
    # Prepare a list of loans with the required details
    loan_list = [{
        'id': loan.id,
        'customer_name': loan.customer_name,
        'book_name': loan.book_name,
        'loan_date': loan.loan_date.isoformat(),
        'return_date': loan.return_date.isoformat()
    } for loan in loans]
    # Return the list of loans as JSON
    return jsonify(loans=loan_list)

# Route to create a new loan, handling both POST and OPTIONS for CORS preflight
@loans_api.route('/', methods=['POST', 'OPTIONS'])
def create_loan():
    if request.method == 'OPTIONS':
        # Respond to CORS preflight with necessary headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    # Get JSON data sent with the POST request
    data = request.get_json()
    # Fetch the customer and book from the database
    customer = Customer.query.get(data['customer_id'])
    book = Book.query.filter_by(name=data['book_name'], status='available').first()

    # Check if the customer and book exist and are available
    if not customer or not book:
        return jsonify({'error': 'Customer or Book not found or not available.'}), 404

    try:
        # Create a new Loan object with the provided data
        new_loan = Loan(
            customer_name=customer.name,
            book_name=book.name,
            loan_date=data['loan_date'],
            return_date=data['return_date'],
            original_author=book.author,
            original_year_published=book.year_published,
            original_book_type=book.book_type
        )
        # Add the new loan to the session and commit the changes to the database
        db.session.add(new_loan)
        book.status = 'loaned'  # Update the status of the book to indicate it is loaned
        db.session.commit()
        return jsonify({'id': new_loan.id}), 201  # Return the ID of the new loan
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': f'Error creating loan: {str(e)}'}), 500

# Route to delete a loan
@loans_api.route('/<int:loan_id>/', methods=['DELETE'])
def delete_loan(loan_id):
    # Find the loan with the given ID
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    try:
        # If the loan is found, create a new Book object to add it back to the database
        book = Book(
            name=loan.book_name,
            author=loan.original_author,
            year_published=loan.original_year_published,
            book_type=loan.original_book_type,
            status='available'  # Update status to available
        )
        # Add the book and delete the loan from the database
        db.session.add(book)
        db.session.delete(loan)
        db.session.commit()  # Commit the changes
        return jsonify({'message': 'Loan deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting loan: {str(e)}'}), 500

# Route to get loan details
@loans_api.route('/<int:loan_id>/', methods=['GET'])
def get_loan_details(loan_id):
    # Find the loan with the given ID
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Prepare the loan data to return
    loan_data = {
        'id': loan.id,
        'customer_name': loan.customer_name,
        'book_name': loan.book_name,
        'loan_date': loan.loan_date.isoformat(),
        'return_date': loan.return_date.isoformat()
    }
    # Return the loan data as JSON
    return jsonify(loan=loan_data)
