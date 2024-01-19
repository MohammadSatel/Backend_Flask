# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields import DateField
from wtforms.validators import DataRequired


# Flask forms (wtforms) allow you to easily create forms in format:
class CreateLoan(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    book_name = StringField('Book Name', validators=[DataRequired()])
    loan_date = DateField('Loan Date', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])

    # Fields for capturing original book details
    original_author = StringField('Original Author', validators=[DataRequired()])
    original_year_published = IntegerField('Original Year Published', validators=[DataRequired()])
    original_book_type = StringField('Original Book Type', validators=[DataRequired()])

    submit = SubmitField('Create Loan')

