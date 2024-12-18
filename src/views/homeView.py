from flask import redirect, render_template, url_for

from ..models.model import RoleType
from ..routers._layout import BASE_URL 


def home():
    nav_data = {
        'page_title': 'Home',
        'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': BASE_URL, 'active': True},
            {'text': 'Contact', 'url': '/contact', 'active': False}
        ],
        'logout': False
        
    }
    isRole = RoleType.query.all()
    print(isRole)
    if len(isRole) == 0:
        return redirect(url_for('role_create'))
    return render_template('home.html',**nav_data)