from flask import render_template, request, url_for

from ..routers._layout import BASE_URL
from ..forms.authForm import CustomerSignUpForm, ServiceProviderSignUpForm , LoginForm


def loginView():
    nav_data = {
        'page_title': 'Login',
        'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': BASE_URL, 'active': True},
            {'text': 'Contact', 'url': '/contact', 'active': False}
        ],
        'logout': False
    }
    username = password = ''
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
    return render_template('auth/login/login.html',form=loginForm,
                            username=username,password=password,
                            **nav_data)

def sigupView(userType):
    previous_url = request.referrer or BASE_URL
    if userType not in ['default','customer','professional']:
        return "Invalid User Type"
    print(userType)
    if userType == 'default':
        nav_data = {
        'page_title': 'Signup',
        'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': BASE_URL, 'active': True},
            {'text': 'Contact', 'url': '/contact', 'active': False}
        ],
        'logout': False
        }
        return render_template('auth/signup/default.html',**nav_data)
    if userType == 'customer':
        nav_data = {
            'page_title': 'Register',
            'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': False},
            'nav_items': [
                {'text': '<-Back', 'url': previous_url, 'active': True},
            ],
            'logout': False
        }
        name = email = password = city = state = country = postalCode = addressDescription = ''
        signupForm = CustomerSignUpForm()
        if signupForm.validate_on_submit():
            name = signupForm.name.data
            email = signupForm.email.data
            password = signupForm.password.data
            city = signupForm.city.data
            state = signupForm.state.data
            country = signupForm.country.data
            postalCode = signupForm.postal_code.data
            addressDescription = signupForm.address_description.data
            print(name,email,password,city,state,country,postalCode,addressDescription)
            return signupForm
        return render_template('auth/signup/customer.html',form=signupForm,
                            name=name,email=email,password=password,
                            city=city,state=state,country=country,
                            postalCode=postalCode,addressDescription=addressDescription,**nav_data)
    if userType == 'professional':
        nav_data = {
            'page_title': 'Register',
            'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': False},
            'nav_items': [
                {'text': '<-Back', 'url': previous_url, 'active': True},
            ]
        }
        name = email = password = city = state = country = postalCode = addressDescription = categoty = service_name = description =   ''
        signupForm = ServiceProviderSignUpForm()
        if signupForm.validate_on_submit():
            name = signupForm.name.data
            email = signupForm.email.data
            password = signupForm.password.data
            city = signupForm.city.data
            state = signupForm.state.data
            country = signupForm.country.data
            postalCode = signupForm.postal_code.data
            addressDescription = signupForm.address_description.data
            categoty = signupForm.categoty.data
            service_name = signupForm.service_name.data
            description = signupForm.description.data
            return signupForm
        return render_template('auth/signup/professional.html',form=signupForm,
                            name=name,email=email,password=password,city=city,state=state,country=country,
                            postalCode=postalCode,addressDescription=addressDescription,
                            categoty=categoty,service_name=service_name,description=description,
                            **nav_data)
