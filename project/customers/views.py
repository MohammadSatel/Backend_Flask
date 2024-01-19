from flask import Blueprint, request, jsonify
from project import db
from project.customers.models import Customer

# Blueprint for customers API
customers_api = Blueprint('customers_api', __name__, url_prefix='/api/customers')

# Route to fetch customers in JSON format
@customers_api.route('/', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    customer_list = [{'id': customer.id, 'name': customer.name, 'city': customer.city, 'age': customer.age} for customer in customers]
    return jsonify(customers=customer_list)

# Route to create a new customer
@customers_api.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], city=data['city'], age=data['age'])
    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating customer: {str(e)}'}), 500

# Route to update an existing customer
@customers_api.route('/<int:customer_id>/', methods=['PUT'])
def edit_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    customer.name = data['name']
    customer.city = data['city']
    customer.age = data['age']

    try:
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating customer: {str(e)}'}), 500

# Route to delete a customer
@customers_api.route('/<int:customer_id>/', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting customer: {str(e)}'}), 500

# Route to get customer details
@customers_api.route('/<int:customer_id>/', methods=['GET'])
def get_customer_details(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer_data = {
        'id': customer.id,
        'name': customer.name,
        'city': customer.city,
        'age': customer.age
    }
    return jsonify(customer=customer_data)