from flask import current_app as app

from ..routers._layout import *
from ..views.adminView import AdminCategoryView, AdminCustomerView, AdminHomeView, AdminSearchView, AdminServiceView

#Admin Controllers Route

#Admin Views Route
@app.route(ADMIN_GET_URL, methods=['GET', 'POST'])
def admin_route_view(userName):
    return AdminHomeView(userName)

@app.route(ADMIN_GET_SERVICE_URL, methods=['GET', 'POST'])
def admin_service_route_view(userName):
    return AdminServiceView(userName)

@app.route(ADMIN_GET_CUSTOMER_URL, methods=['GET', 'POST'])
def admin_customer_route_view(userName,action,id):
    return AdminCustomerView(userName,action,id)


@app.route(ADMIN_GET_CATEGORY_URL, methods=['GET', 'POST','PUT'])
def admin_category_route_view(userName,action,id):
    return AdminCategoryView(userName,action,id)

@app.route(ADMIN_GET_SEARCH_URL, methods=['GET', 'POST'])
def admin_search_route_view(userName,action,id):
    return AdminSearchView(userName,action,id)