from flask_wtf import FlaskForm 
from wtforms import  DateField, SelectField, StringField ,SubmitField ,IntegerField
from wtforms.validators import DataRequired ,email,Length


class SearchProfessionalForm(FlaskForm):
   input = StringField('Input',validators=[DataRequired()],render_kw={"placeholder":"Input"})
   search_by = SelectField(
       'Search By',
       choices=[
            ('username', 'Username'),
           ('category', 'Category')
       ],
       validators=[DataRequired()],
       render_kw={'class': 'mr-3'}
   )
   search = SubmitField('Search',render_kw={"class": "btn btn-dark btn-block h-10"})