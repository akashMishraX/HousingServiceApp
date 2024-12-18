from flask import render_template, request

from ..routers._layout import BASE_URL


def errorNotFound(message):
    previous_url = request.referrer or BASE_URL
    nav_data = {
            'page_title': 'Register',
            'site_title': {'name': '', 'url':'', 'active': False},
            'nav_items': [
                {'text': '<-Back', 'url': previous_url, 'active': True},
            ],
            'logout': False,
            'message':f'{message}'
    }
    return render_template('error/not_found.html',**nav_data)