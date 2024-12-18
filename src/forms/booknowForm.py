from flask_wtf import FlaskForm 
from wtforms import  DateField, SelectField, StringField ,SubmitField ,IntegerField
from wtforms.validators import DataRequired ,email,Length


class BookNowForm(FlaskForm):
   expected_date = DateField('Expected Date',validators=[DataRequired()],render_kw={"placeholder":"Expected Date"})
   book = SubmitField('Book',render_kw={"class": "btn btn-dark btn-block"})