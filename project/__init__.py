import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

# Database Setup
app = Flask(__name__, static_folder='../Frontend_Vue/client/dist', static_url_path='')

app.config['SECRET_KEY'] = 'supersecret'
app.config['TEMPLATES_AUTO_RELOAD'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # This allows all origins for all routes under /api/

# Register Blueprints
from project.books.views import books_api
from project.customers.views import customers_api
from project.loans.views import loans_api

app.register_blueprint(books_api, url_prefix='/api/books')
app.register_blueprint(customers_api, url_prefix='/api/customers')
app.register_blueprint(loans_api, url_prefix='/api/loans')

# The route for serving Vue.js app is defined in app.py
