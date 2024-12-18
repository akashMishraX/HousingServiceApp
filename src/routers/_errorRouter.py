from flask import current_app as app
from src.routers._layout import *
from src.views.errorView import errorNotFound


# Customer Controllers Route


#Customer Views Route
@app.route(ERROR_GET_URL,methods=['GET'])
def error_route_view(message):return errorNotFound(message)