from flask_wtf import FlaskForm 
from wtforms import  DateField, SelectField, StringField ,SubmitField ,IntegerField
from wtforms.validators import DataRequired ,email,Length


class AcceptForm(FlaskForm):
   appointment_date = DateField('Appointment Date',validators=[DataRequired()],render_kw={"placeholder":"Appointment Date"})
   completion_date = DateField('Completion Date',validators=[DataRequired()],render_kw={"placeholder":"Completion Date"})
   accept = SubmitField('Accept',render_kw={"class": "btn btn-dark btn-block"})