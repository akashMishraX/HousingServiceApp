from flask import current_app as app
from src.routers._layout import *
from ..views.professionalView import professionalHomeView, professionalProfileView, professionalRequestSView, professionalRequestServiceView


#Professional Controllers Route


#Professional Views Route
@app.route(SERVICE_GET_URL,methods=['GET'])
def professional_route_view(userName):return professionalHomeView(userName)


@app.route(SERVICE_GET_PROFILE_URL,methods=['GET','POST'])
def professional_profile_route_view(userName):return professionalProfileView(userName)


@app.route(SERVICE_REQUEST_SERVICE_URL,methods=['GET','POST'])
def professional_request_service_route_view(serviceUserName,customerUserName,request):return professionalRequestServiceView(serviceUserName,customerUserName,request)

@app.route(SERVICE_REQUEST_BUTTON_URL,methods=['GET','POST'])
def professional_request_view(serviceUserName,customerUserName,request):return professionalRequestSView(serviceUserName,customerUserName,request)