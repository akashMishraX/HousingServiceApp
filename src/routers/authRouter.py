from flask import current_app as app
from src.routers._layout import *
from src.controllers.authController import loginController ,signupController
from src.views.authView import loginView,sigupView


#Auth Controllers Route
@app.route(LOGIN_POST_URL,methods=['POST'])
def login_route_controller():return loginController()

@app.route(SIGNUP_POST_URL,methods=['POST'])
def signup_route_controller(userType):return signupController(userType)



#Auth Views Route
@app.route(LOGIN_GET_URL,methods=['GET'])
def login_route_view():return loginView()

@app.route(SIGNUP_GET_URL,methods=['GET'])
def signup_route_view(userType):return sigupView(userType)

