from flask_wtf import FlaskForm 
from wtforms import  SelectField, StringField ,SubmitField ,IntegerField
from wtforms.validators import DataRequired ,email,Length

from ..models.model import Category

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired()])
    login = SubmitField('Login',render_kw={"class": "btn btn-dark btn-block"})

class CustomerSignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)],render_kw={"placeholder":"Username"})
    password = StringField('Password',validators=[DataRequired(),Length(min=5,max=20)],render_kw={"placeholder":"Password"})
    name = StringField('Name',validators=[DataRequired()],render_kw={"placeholder":"Name"})
    email = StringField('Email',validators=[DataRequired(),email()],render_kw={"placeholder":"Email"})
    phone_number = IntegerField('Phone Number',validators=[DataRequired(),Length(min=10,max=10)],render_kw={"placeholder":"Phone Number"})
    city = StringField('City',validators=[DataRequired()],render_kw={"placeholder":"City"})
    state = StringField('State',validators=[DataRequired()],render_kw={"placeholder":"State"})
    country = StringField('Country',validators=[DataRequired()],render_kw={"placeholder":"Country"})
    postal_code = StringField('Postal Code',validators=[DataRequired()],render_kw={"placeholder":"Postal Code"})
    address_description = StringField('Address Description',validators=[DataRequired()],render_kw={"placeholder":"Address Description"})
    register = SubmitField('Register as Customer',render_kw={"class": "btn btn-dark btn-block"})

categories = Category.query.filter_by().all()
data = [(category.name.lower(),category.name.lower()) for category in categories]


class ServiceProviderSignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)],render_kw={"placeholder":"Username"})
    password = StringField('Password',validators=[DataRequired(),Length(min=5,max=20)],render_kw={"placeholder":"Password"})
    name = StringField('Name',validators=[DataRequired()],render_kw={"placeholder":"Name"})
    email = StringField('Email',validators=[DataRequired(),email()],render_kw={"placeholder":"Email"})
    phone_number = IntegerField('Phone Number',validators=[DataRequired(),Length(min=10,max=10)],render_kw={"placeholder":"Phone Number"})
    city = StringField('City',validators=[DataRequired()],render_kw={"placeholder":"City"})
    state = StringField('State',validators=[DataRequired()],render_kw={"placeholder":"State"})
    country = StringField('Country',validators=[DataRequired()],render_kw={"placeholder":"Country"})
    postal_code = StringField('Postal Code',validators=[DataRequired()],render_kw={"placeholder":"Postal Code"})
    address_description = StringField('Address Description',validators=[DataRequired()],render_kw={"placeholder":"Address Description"})
    category = SelectField(
        'Category',
        choices=data,
        validators=[DataRequired()],
        render_kw={"placeholder": "Service Name"}
    )
    service_name = StringField('Service Name',validators=[DataRequired()],render_kw={"placeholder":"Service Name"})
    description = StringField('Description',validators=[DataRequired()],render_kw={"placeholder":"Description"})
    register = SubmitField('Register as Service Professional',render_kw={"class": "btn btn-dark btn-block"})

