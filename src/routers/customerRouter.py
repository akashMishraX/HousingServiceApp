from flask import current_app as app
from ..routers._layout import *
from ..views.customerView import bookingView, customerHomeView, customerProfileView, customerRateView, customerRequesServicetView, customerRequestView, customerSearchView

# Customer Controllers Route


#Customer Views Route
@app.route(CUSTOMER_GET_URL,methods=['GET','POST'])
def customer_route_view(userName):return customerHomeView(userName)

@app.route(CUSTOMER_GET_PROFILE_URL,methods=['GET','POST'])
def customer_profile_route_view(userName):return customerProfileView(userName)

@app.route(CUSTOMER_GET_SEARCH_URL,methods=['GET','POST'])
def customer_search_route_view(userName):return customerSearchView(userName)

@app.route(CUSTOMER_REQUEST_SERVICE_URL,methods=['GET','POST'])
def customer_request_service_route_view(customerUserName,action,id):return customerRequesServicetView(customerUserName,action,id)

@app.route(BOOKING_URL,methods=['GET','POST'])
def booking_route_view(customerUserName,serviceUserName,action):return bookingView(customerUserName,serviceUserName,action)

@app.route(CUSTOMER_REQUEST_BUTTON_URL,methods=['GET','POST'])
def customer_request_view(customerUserName,serviceUserName,request):return customerRequestView(customerUserName,serviceUserName,request)


@app.route(CUSTOMER_RATE_URL,methods=['GET','POST'])
def customer_rate_view(customerUserName,requestId,rating):return customerRateView(customerUserName,requestId,rating)