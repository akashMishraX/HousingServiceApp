class Routes:
    def __init__(self, version):
        self.BASE_URL = f'/app/v{version}'
        self.routes = {
            'admin': self.create_route('admin'),
            'services': self.create_route('services'),
            'customer': self.create_route('customer'),
            'error':self.create_route('error'),
            'auth': self.create_route('auth')
        }

    def create_route(self, route):
        return f"{self.BASE_URL}/{route}"

    def create_sub_route(self, base_name, sub_route):
        if base_name not in self.routes:
            raise ValueError(f"Base route '{base_name}' does not exist")
        return f"{self.routes[base_name]}/{sub_route}"


routes =  Routes(version='0')
BASE_URL = routes.create_route('')
BASE_URL_ADMIN = routes.create_route('admin')
BASE_URL_SERVICES = routes.create_route('services')
BASE_URL_CUSTOMER = routes.create_route('customer')
BASE_URL_AUTH = routes.create_route('auth')
#AUTH ROUTES
LOGIN_POST_URL = routes.create_sub_route('auth','login/')
LOGIN_GET_URL = routes.create_sub_route('auth','login')

SIGNUP_POST_URL = routes.create_sub_route('auth','signup/<userType>')
SIGNUP_GET_URL = routes.create_sub_route('auth','signup/<userType>')

#ERROR ROUTES
ERROR_GET_URL = routes.create_sub_route('error','<message>')

#ADMIN ROUTES
ADMIN_GET_URL = routes.create_sub_route('admin', '<userName>')
ADMIN_GET_SERVICE_URL = routes.create_sub_route('admin', '<userName>/service')
ADMIN_GET_CUSTOMER_URL = routes.create_sub_route('admin', '<userName>/<action>/customer/<id>')
ADMIN_GET_CATEGORY_URL = routes.create_sub_route('admin', '<userName>/<action>/category/<id>')
ADMIN_GET_SEARCH_URL = routes.create_sub_route('admin', '<userName>/<action>/search/<id>')

#CUSTOMER ROUTES
CUSTOMER_GET_URL = routes.create_sub_route('customer','<userName>')
CUSTOMER_GET_PROFILE_URL = routes.create_sub_route('customer','<userName>/profile')
CUSTOMER_GET_SEARCH_URL = routes.create_sub_route('customer','<userName>/search')
CUSTOMER_GET_SUMMARY_URL = routes.create_sub_route('customer','<userName>/summary')
CUSTOMER_REQUEST_SERVICE_URL = routes.create_sub_route('customer','<customerUserName>/<action>/request/<id>')
BOOKING_URL = routes.create_sub_route('customer','<customerUserName>/<serviceUserName>/<action>/booking')
CUSTOMER_REQUEST_BUTTON_URL = routes.create_sub_route('customer','<customerUserName>/<serviceUserName>/<request>/booking')
CUSTOMER_RATE_URL =  routes.create_sub_route('customer','<customerUserName>/<requestId>/rate/<rating>')

#SERVICES ROUTES
SERVICE_GET_URL = routes.create_sub_route('services','<userName>')
SERVICE_GET_PROFILE_URL = routes.create_sub_route('services','<userName>/profile')
SERVICE_GET_SUMMARY_URL = routes.create_sub_route('services','<userName>/summary')
SERVICE_REQUEST_SERVICE_URL = routes.create_sub_route('services','<serviceUserName>/<customerUserName>/<request>')
SERVICE_REQUEST_BUTTON_URL = routes.create_sub_route('services','<serviceUserName>/<customerUserName>/<request>/button')

