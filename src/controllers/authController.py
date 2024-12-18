from flask import redirect, request, url_for

from ..models.modelFunctions import create_customer, create_service_professional
from ..routers._layout import *
from ..models.model import *

from ..utils.helperResponseHandler import ApiResponse
from ..utils.helperErrorHandler import ApiError


def loginController():
    data = request.form.to_dict()
    try:
        user = User.query.filter_by(username=data['username']).first()
        role  = RoleType.query.filter_by(id=user.roleId).first()

        if user is None or role is None:
            return redirect(url_for('error_route_view',message='User Not Found'))
        elif role.name.value == 'Customer':
            if user.username != data['username'] or user.password != data['password']:
                return redirect(url_for('error_route_view',message='Login credential is invalid'))
            return redirect(url_for('customer_route_view',userName=user.username))
        elif role.name.value == 'ServiceProfessional':
            if user.username != data['username'] or user.password != data['password']:
                return redirect(url_for('error_route_view',message='Login credential is invalid'))
            return redirect(url_for('professional_route_view',userName=user.username))
        elif role.name.value == 'Admin':
           
            if user.username != data['username'] or user.password != data['password']:
                print(user.username,user.password)
                return redirect(url_for('error_route_view',message='Login credential is invalid'))
            return redirect(url_for('admin_route_view', userName=user.username))
        else:
            return redirect(url_for('error_route_view',message='User Not Found'))
    except Exception as e:
        print(e)
        return ApiError.internal_server_error(f'Internal Server Error {e}')
   



def signupController(userType):
    if userType not in ['customer','professional']:
        return ApiError.bad_request('Invalid User Type')
    if userType == 'customer':
        data = request.form.to_dict()
        try:
            user = User.query.filter_by(username=data['username']).first()
            if user:
                return ApiError.bad_request('User Already Exists')
            create_customer(data)
            return redirect(url_for('login_route_view'))
        except Exception as e:
            print(e)
            return ApiError.internal_server_error(f'Internal Server Error :-{e}')
    if userType == 'professional':
        data = request.form.to_dict()
        try:
            user = User.query.filter_by(username=data['username']).first()
            if user:
                return ApiError.bad_request('User Already Exists')
            # return f'{data}'
            create_service_professional(data)
            return redirect(url_for('login_route_view'))
        except Exception as e:
            print(e)
            return ApiError.internal_server_error(f'Internal Server Error :-{e}')


