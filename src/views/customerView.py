from flask import jsonify, redirect, render_template, request, url_for

from ..forms.rateService import RateForm

from ..forms.searchBoxForm import SearchForm

from ..utils.helperErrorHandler import ApiError

from ..models.modelFunctions import addRating, cancel_appointment, request_service

from ..models.model import AssignedService, Category, ServiceProfessional, ServiceRequested, User, UserAddress

from ..forms.booknowForm import BookNowForm
from ..routers._layout import BASE_URL, CUSTOMER_GET_PROFILE_URL, CUSTOMER_GET_SEARCH_URL, CUSTOMER_GET_SUMMARY_URL


def customerHomeView(userName):
    data_from_sp = ServiceProfessional.query.all()
    all_category = []
    category_dict = {}
    for service in data_from_sp:
        if service.isApproved==False or service.isAvailable == False:continue

        serviceUser = User.query.filter_by(id=service.id).first()
        category = Category.query.filter_by(id=service.categoryId).first()
        print(category)
        service_data = {
            'service_name': service.serviceName,
            'description': service.description,
            'price': category.pricing,
            'userName': serviceUser.username
        }
        if category.name not in category_dict:
            category_dict[category.name] = {
                'category': {
                    'name': category.name,
                    'services': []
                }
        }
        # Add the service to the appropriate category
        category_dict[category.name]['category']['services'].append(service_data)
    for category, data in category_dict.items():
        all_category.append(data)

    # Sort the top services by rating
    top_services = []
    service_data = {}
    data_from_sp.sort(key=lambda x: x.serviceRating, reverse=True)
    for service in data_from_sp:
        if service.isApproved==False or service.isAvailable == False:continue

        serviceUser = User.query.filter_by(id=service.id).first()
        category = Category.query.filter_by(id=service.categoryId).first()
        service_data['service'] = {
            'username': serviceUser.username,
            'name': service.serviceName,
            'category': category.name,
            'description': service.description,
            'price': category.pricing,
            'rating': service.serviceRating,
            'userName': serviceUser.username
        }
        top_services.append(service_data)
        service_data = {}

    nav_data = {
        'page_title': 'Customer',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Profile', 'url': url_for('customer_profile_route_view', userName=userName), 'active': True},
            {'text': 'Search', 'url': url_for('customer_search_route_view', userName=userName), 'active': True},
            {'text':'Request','url':url_for('customer_request_service_route_view',customerUserName=userName,action='view',id=0),'active':True}
        ],
        'logout': True,
        'all_category':all_category,
        'top_services':top_services
    }
    return render_template('customer/home.html',**nav_data, userName=userName)

def customerProfileView(userName):
    customer = User.query.filter_by(username=userName).first()
    print(customer.id)
    customer_details ={
            'username':customer.username,
            'email':customer.email,
            'phone':customer.phoneNumber,
    }
    past_services = []
    sr = ServiceRequested.query.filter_by(customerId=customer.id).all()
    for s in sr:
        service = User.query.filter_by(id=s.serviceProfessionalId).first()
        serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
        aS = AssignedService.query.filter_by(id=s.id).first()
        category = Category.query.filter_by(id=serviceP.categoryId).first()
        if s.serviceStatus.value == 'Rejected':
             obj = {'username':service.username,'serviceName':serviceP.serviceName,'category':category.name,'rating':'N/A','feedback':'N/A','email':service.email,'phone':service.phoneNumber,'address':' ','status':s.serviceStatus.value},
             past_services.append(obj[0])
             continue
        if aS is None:continue
        if aS.rating is None:rating = 'Not provided yet'
        if aS.feedback is None:feedback = 'Not provided yet'
        if aS.workStatus.value != 'Pending':
            if aS.rating is not None:rating = aS.rating.value
            if aS.feedback is not None:feedback = aS.feedback
            
            
            obj = {'username':service.username,'serviceName':serviceP.serviceName,'category':category.name,'rating':rating,'feedback':feedback,'email':service.email,'phone':service.phoneNumber,'address':' ','status': aS.workStatus.value}
            past_services.append(obj)
    # return jsonify(past_services)   
    appoinments = []
    sr = ServiceRequested.query.filter_by(customerId=customer.id).all()
    for s in sr:
        service = User.query.filter_by(id=s.serviceProfessionalId).first()
        serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
        category = Category.query.filter_by(id=serviceP.categoryId).first()
        aS = AssignedService.query.filter_by(id=s.id).first()
        if aS is None:continue
        if aS.workStatus.value == 'Pending':
            obj = {'username':service.username,'serviceName':serviceP.serviceName,'appoinmentDate':aS.appointmentDate.strftime("%Y-%m-%d"),'price':category.pricing,'status':aS.workStatus.value},
            appoinments.append(obj[0])

    
    # return past_services
    nav_data = {
        'page_title': 'Customer',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('customer_route_view', userName=userName), 'active': True},
            {'text': 'Search', 'url': url_for('customer_search_route_view', userName=userName), 'active': True},
            {'text':'Request','url':url_for('customer_request_service_route_view',customerUserName=userName,action='view',id=0),'active':True}
        ],
        'logout': True,
        'customer_deatil':customer_details,
        'past_services':past_services,
        'service_appionment':appoinments
    }
    return render_template('customer/profile.html',userName=userName,**nav_data)

def customerSearchView(userName):
    nav_data = {
        'page_title': 'Customer',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('customer_route_view', userName=userName), 'active': True},
            {'text': 'Profile', 'url': url_for('customer_profile_route_view', userName=userName), 'active': True},
            {'text':'Request','url':url_for('customer_request_service_route_view',customerUserName=userName,action='view',id=0),'active':True}
        ],
        'logout': True
    }
    nav_data['search_data'] = []
    form = SearchForm()
    input = search_by = ''
    if form.validate_on_submit():
        input = form.input.data
        search_by = form.search_by.data

    if request.method == 'POST':
        if search_by == 'category':
            category = Category.query.filter_by(name=input).first()
            if category is None:
                    return ApiError.bad_request('No Such Category Found')
            data_from_sp = ServiceProfessional.query.filter_by(categoryId=category.id).all()
            if len(data_from_sp) == 0:
                return ApiError.bad_request('No Service Found')
            for data in data_from_sp:
                if data.isApproved==False or data.isAvailable == False:continue
                service = User.query.filter_by(id=data.id).first()
                category = Category.query.filter_by(id=data.categoryId).first()
                obj={
                    'username':service.username,
                    'service_name':data.serviceName,
                    'category':category.name,
                    'description':data.description,
                    'price':category.pricing,
                    'rating':data.serviceRating
                }
                nav_data['search_data'].append(obj)
            if len(data_from_sp) != 0:
                return render_template('customer/search.html',**nav_data,form=form, input=input, search_by=search_by,userName=userName)
        elif search_by == 'rating':
            data_from_sp = ServiceProfessional.query.filter_by(serviceRating=input).all()
            for data in data_from_sp:
                if data.isApproved==False or data.isAvailable == False:continue
                service = User.query.filter_by(id=data.id).first()
                category = Category.query.filter_by(id=data.categoryId).first()
                obj={
                    'username':service.username,
                    'service_name':data.serviceName,
                    'category':category.name,
                    'description':data.description,
                    'price':category.pricing,
                    'rating':data.serviceRating
                }
                nav_data['search_data'].append(obj)
            if len(data_from_sp) != 0:
                return render_template('customer/search.html',form=form, input=input, search_by=search_by,userName=userName,**nav_data)
        
        elif search_by == 'city':
            addre = UserAddress.query.filter_by(city=input.capitalize()).all()
            service = User.query.filter_by().all()
            for a in addre:
                data_from_sp = ServiceProfessional.query.filter_by(id=a.userId).all()
                for data in data_from_sp:
                    if data.isApproved==False or data.isAvailable == False:continue
                    service = User.query.filter_by(id=data.id).first()
                    category = Category.query.filter_by(id=data.categoryId).first()
                    obj={
                        'username':service.username,
                        'service_name':data.serviceName,
                        'category':category.name,
                        'description':data.description,
                        'price':category.pricing,
                        'rating':data.serviceRating
                    }
                    nav_data['search_data'].append(obj)
                if len(data_from_sp) != 0:
                    return render_template('customer/search.html',**nav_data,form=form, input=input, search_by=search_by,userName=userName)
        else:
            return render_template('error/not_found.html',**nav_data,form=form, input=input, search_by=search_by,userName=userName)
    return render_template('customer/search.html',**nav_data,form=form, input=input, search_by=search_by,userName=userName)


def customerRequesServicetView(customerUserName,action,id):
    if action == 'cancel':
        print(id)
        sR = ServiceRequested.query.filter_by(id=id).first()
        serviceUserName = User.query.filter_by(id=sR.serviceProfessionalId).first().username
        print(sR,serviceUserName)
        res = cancel_appointment(customerUserName,serviceUserName)
        # if not res:
        #     return ApiError.internal_server_error('Unable to make service completed')
        return redirect(url_for('customer_request_service_route_view',customerUserName=customerUserName,action='view',id=0))
    all_request = []
    customer = User.query.filter_by(username=customerUserName).first()
    sr = ServiceRequested.query.filter_by(customerId=customer.id).all()
    for s in sr:
        service = User.query.filter_by(id=s.serviceProfessionalId).first()
        serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
        category =Category.query.filter_by(id=serviceP.categoryId).first()
        assignedS = AssignedService.query.filter_by(id=s.id).first()
        workStatus = 'Not yet accepted'
        isAccepted = False
        isEditable = False
        isCancelable = False
        isRateable=False
        if s.serviceStatus.value == 'Accepted':
            isAccepted = True
            if assignedS is None:continue
            workStatus = assignedS.workStatus.value
            if workStatus == 'Pending':isEditable =isCancelable = True
            if workStatus == 'Completed':isRateable = True
            if assignedS.rating is not None:
                isRateable = False
            if s.serviceStatus.value == 'Pending':
                isEditable = True
                isCancelable = True

        elif s.serviceStatus.value == 'Pending':
            isEditable = True
            isCancelable = True
        obj={
            'info':{
                'requestId':s.id,
                'username':service.username,
                'serviceName':serviceP.serviceName,
                'category':category.name,
                'price':category.pricing,
                'rating':serviceP.serviceRating,
                'customerName':customerUserName
            },
            'isAccepted':isAccepted,
            'workStatus':workStatus,
            'isEditable':isEditable,
            'isCancelable':isCancelable,
            'isRateable':isRateable
        }

        all_request.append(obj)
    # return jsonify({'all_request':all_request})
    nav_data = {
        'page_title': 'Customer',
        'site_title': {'name': f'{customerUserName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('customer_route_view', userName=customerUserName), 'active': True},
            {'text': 'Profile', 'url': url_for('customer_profile_route_view', userName=customerUserName), 'active': True},
            {'text': 'Search', 'url': url_for('customer_search_route_view', userName=customerUserName), 'active': True},
        ],
        'logout': True,
        'all_request':all_request
    }
    return render_template('customer/request.html',**nav_data)



def bookingView(customerUserName,serviceUserName,action):
    if request.method == 'POST':
        data = {
            'customerUserName':customerUserName,
            'serviceUserName':serviceUserName,
            'expected_date': request.form['expected_date']
        }
        
        res = request_service(data,action)
        if not res:
            return ApiError.internal_server_error('Failed to book service as Service is pending')
        return redirect(url_for('customer_request_service_route_view',customerUserName=customerUserName,action='view',id=0))
    previous_url = request.referrer or BASE_URL
    if action == 'book':

        
        data_from_user = User.query.filter_by(username=serviceUserName).first()
        data_from_sp = ServiceProfessional.query.filter_by(id=data_from_user.id).first()
        if data_from_sp.isApproved==False or data_from_sp.isAvailable == False: return ApiError.internal_server_error('Service is not approved')
        category = Category.query.filter_by(id=data_from_sp.categoryId).first()
        expected_date =''
        form = BookNowForm()
    
    if action == 'edit':
        data_from_user = User.query.filter_by(username=serviceUserName).first()
        data_from_customer = User.query.filter_by(username=customerUserName).first()
        data_from_sp = ServiceProfessional.query.filter_by(id=data_from_user.id).first()
        if data_from_sp.isApproved==False or data_from_sp.isAvailable == False: return ApiError.internal_server_error('Service is not approved')
        category = Category.query.filter_by(id=data_from_sp.categoryId).first()
        req = ServiceRequested.query.filter_by(serviceProfessionalId=data_from_user.id,serviceStatus='Pending',customerId=data_from_customer.id).first()
        if req is None: return ApiError.internal_server_error('No Pending Request Found')
        expected_date = req.expectedDate
        print(req)
        form = BookNowForm(
            expected_date = expected_date
        )
    
    nav_data = {
        'page_title': 'Booking',
        'site_title': {'name': f'{serviceUserName}', 'url': '', 'active': False},
        'nav_items': [
            {'text': '< Back', 'url': previous_url,'active': True},
        ],
        'logout': True,
        'service_data':{
            'username':data_from_user.username,
            'email':data_from_user.email,
            'phone':data_from_user.phoneNumber,
            'serviceName':data_from_sp.serviceName,
            'description':data_from_sp.description,
            'rating':data_from_sp.serviceRating,
            'pricing':category.pricing,
            'action':action
        }
    }
    
    
    if form.validate_on_submit():
        expected_date = form.expected_date.data
    return render_template('customer/booking.html',
                           form=form,
                           expected_date=expected_date,
                           customerUserName=customerUserName,
                           serviceUserName=serviceUserName,
                           action=action,
                           **nav_data)
def customerRateView(customerUserName,requestId,rating):
    previous_url = request.referrer or BASE_URL
    nav_data = {
        'page_title': 'Rating',
        'site_title': {'name': f'{customerUserName}', 'url': '', 'active': False},
        'nav_items': [
            {'text': '< Back', 'url': previous_url,'active': True},
        ],
        'logout': True,
        'info':{
            'customerUserName':customerUserName,
            'requestId':requestId,
            'rating':rating,
        }
    }
    rating = feedback  =''
    form = RateForm()
    if form.validate_on_submit():
        rating = form.rating.data
        feedback = form.feedback.data

    print(rating,feedback)
    rating_arr = ['One','Two','Three','Four','Five']
    if rating in rating_arr:
        addRating(requestId,rating,feedback)
        return redirect(url_for('customer_request_service_route_view',customerUserName=customerUserName,action='view',id=0))
    return render_template('customer/rating.html',
                            form=form,
                          rating=rating,
                          feedback=feedback,
                          **nav_data)






def customerRequestView(customerUserName,serviceUserName,req):
   pass