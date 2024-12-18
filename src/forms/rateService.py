from flask_wtf import FlaskForm 
from wtforms import  DateField, SelectField, StringField ,SubmitField ,IntegerField
from wtforms.validators import DataRequired ,email,Length


class RateForm(FlaskForm):
    rating = SelectField(
       'Rating',
       choices=[
           ('One', 'One'),
           ('Two', 'Two'),
           ('Three', 'Three'),
           ('Four', 'Four'),
           ('Five', 'Five'),
       ],
       validators=[DataRequired()],
       render_kw={'class': 'mr-3'}
    )
    feedback = StringField('Feedback',validators=[DataRequired()],render_kw={"placeholder":"Feedback"})
    submit_exp = SubmitField('Submit',render_kw={"class": "btn btn-dark btn-block"})