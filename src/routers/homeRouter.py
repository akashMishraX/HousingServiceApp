from flask import current_app as app
from src.routers._layout import BASE_URL
from src.views.homeView import home

@app.route(BASE_URL,methods=['GET'])
def index():return home()

