from flask_wtf import FlaskForm 
from wtforms import StringField ,SubmitField 
from wtforms.validators import DataRequired 


class CreateCategory(FlaskForm):
   name = StringField('Category Name',validators=[DataRequired()],render_kw={"placeholder":"Category Name"})
   pricing = StringField('Pricing',validators=[DataRequired()],render_kw={"placeholder":"Pricing"})
   time_required = StringField('Time Required',validators=[DataRequired()],render_kw={"placeholder":"Time Required"})
   Create = SubmitField('Create',render_kw={"class": "btn btn-dark btn-block"})

class EditCategory(FlaskForm):
   name = StringField('Category Name',validators=[DataRequired()],render_kw={"placeholder":"Category Name"})
   pricing = StringField('Pricing',validators=[DataRequired()],render_kw={"placeholder":"Pricing"})
   time_required = StringField('Time Required',validators=[DataRequired()],render_kw={"placeholder":"Time Required"})
   save_cahnge= SubmitField('Save Change',render_kw={"class": "btn btn-dark btn-block"})