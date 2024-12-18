from flask import redirect, render_template, url_for ,request
from ..forms.serviceAcceptanceForm import AcceptForm
from ..utils.helperErrorHandler import ApiError
from ..models.modelFunctions import make_it_accepted, make_it_completed, make_it_rejected, makeServiceAvailabiltyChange, updateRating
from ..models.model import AssignedService, Category, ServiceProfessional, ServiceRequested, User, UserAddress
from ..routers._layout import BASE_URL


def professionalHomeView(userName):
    service = User.query.filter_by(username=userName).first()
    all_req = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Pending').all()
    reqs = []
    req_obj = {}
    for req in all_req:
        customer = User.query.filter_by(id=req.customerId).first()
        service = ServiceProfessional.query.filter_by(id=req.serviceProfessionalId).first()
        req_obj = { 'username':customer.username, 'service_name': service.serviceName , 'expected_date': req.expectedDate.strftime("%Y-%m-%d")},
        reqs.append(req_obj[0])
    
    all_appoinment = []
    serviceRequested = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Accepted').all()
    for s in serviceRequested:
        service = User.query.filter_by(id=s.serviceProfessionalId).first()
        serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
        customer = User.query.filter_by(id=s.customerId).first()
        assignedService = AssignedService.query.filter_by(id=s.id,workStatus='Pending').first()

        if assignedService is None:continue

        obj =  { 'customer_name': customer.username, 'service_name': serviceP.serviceName, 'service_username': service.username,'appoinment_date': assignedService.appointmentDate.strftime("%Y-%m-%d"), 'expected_completion_date': assignedService.completionDate.strftime("%Y-%m-%d")},
        all_appoinment.append(obj[0])
    
    all_completed = []
    serviceRequested = ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()
    for s in serviceRequested:
        service = User.query.filter_by(id=s.serviceProfessionalId).first()
        serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
        customer = User.query.filter_by(id=s.customerId).first()
        assignedService = AssignedService.query.filter_by(id=s.id).first()
        rating = 'N/A'
        if s.serviceStatus.value == 'Rejected':
            obj = {'customer_name':customer.username, 'service_name': serviceP.serviceName, 'appoinment_date': 'N/A', 'completion_date': 'N/A', 'rating': rating,'status':s.serviceStatus.value},
            all_completed.append(obj[0])
            continue
        if assignedService is None:continue
        if assignedService.workStatus.value == 'Pending':continue
        if assignedService.rating is None:rating='N/A'

        obj = {'customer_name':customer.username, 'service_name': serviceP.serviceName, 'appoinment_date': assignedService.appointmentDate.strftime("%Y-%m-%d"), 'completion_date': assignedService.completionDate.strftime("%Y-%m-%d"), 'rating': rating,'status':assignedService.workStatus.value},
        all_completed.append(obj[0])

    nav_data = {
        'page_title': 'Professional',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Profile', 'url': url_for('professional_profile_route_view', userName=userName), 'active': True},
        ],
        'logout': True,
       'all_appoinment':all_appoinment,
        'all_completed':all_completed,
        'all_requested':reqs
        
    }
    return render_template('professional/home.html',**nav_data)

def professionalProfileView(userName):
    service= User.query.filter_by(username=userName).first()
    serviceP = ServiceProfessional.query.filter_by(id=service.id).first()
    addressD = UserAddress.query.filter_by(userId=service.id).first()
    address = f'{addressD.city}, {addressD.state}, {addressD.country}'
    rated = 0
    all_exp = []
    rating = []
    
    reqService = ServiceRequested.query.filter_by(serviceProfessionalId=service.id , serviceStatus='Accepted').all()
    print(reqService)
    for req in reqService:
        serviceRating = 0 
        assignedService = AssignedService.query.filter_by(id=req.id,workStatus='Completed').all()
        if assignedService is None:continue
        print(assignedService)
        for aS in assignedService:
            if aS.rating is not None:
                rating.append(aS.rating.value)

        
        for aS in assignedService:
            serviceP = ServiceProfessional.query.filter_by(id=req.serviceProfessionalId).first()
            customer = User.query.filter_by(id=req.customerId).first()
            category = Category.query.filter_by(id=serviceP.categoryId).first()
            if aS.rating is not None:serviceRating = aS.rating.value
            obj = {
                'exp':f'Worked as {category.name} professional on {aS.appointmentDate.strftime("%Y-%m-%d")}',
                'rating':serviceRating,
                'feedback':aS.feedback,
                'customer':{
                    'username':customer.username,
                    'email':customer.email,
                    'phone':customer.phoneNumber,
                    'address':f'{customer.address.city}, {customer.address.state}, {customer.address.country}',
                    'rating':serviceRating
                    
                }
            }
            all_exp.append(obj)
    if len(rating) != 0:
        print(rating,len(rating))
        rated = sum(rating)/len(rating)
    updateRating(service.id,rated)
    nav_data = {
        'page_title': 'Professional',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('professional_route_view', userName=userName), 'active': True},
        ],
        'logout': True,
        'user_profile_details':{
            'username': service.username,'service_name': serviceP.serviceName, 'rating': serviceP.serviceRating,'email':service.email,'phone':service.phoneNumber,'address':address,'isAvailable':serviceP.isAvailable ,'isApproved':serviceP.isApproved
            },
        'rating':rated,
        'experiences':all_exp,
    }
    return render_template('professional/profile.html',**nav_data)




def professionalRequestServiceView(serviceUserName,customerUserName,req):
    if req == 'reject':
        res = make_it_rejected(serviceUserName,customerUserName)
        if not res:
            return ApiError.internal_server_error('Failed to reject service')
        return redirect(url_for('professional_route_view', userName=serviceUserName))

    if request.method == 'POST':
        res = make_it_accepted(serviceUserName,customerUserName,request.form['appointment_date'],request.form['completion_date'])
        if not res:
            return ApiError.internal_server_error('Failed to accept service')   

        
        return redirect(url_for('professional_route_view', userName=serviceUserName))
    if req == 'accept':
        previous_url = request.referrer or BASE_URL
        nav_data = {
            'page_title': 'Professional',
            'site_title': {'name': f'', 'url': '', 'active': False},
            'nav_items': [
                {'text': '< Back', 'url':previous_url, 'active': True},
            ],
            'logout': True
        }
        form = AcceptForm()
        appointment_date = completion_date= ''
        if form.validate_on_submit():
            appointment_date = form.appointment_date.data
            completion_date = form.completion_date.data
            
        return render_template('professional/acceptRejectService.html',
                                serviceUserName=serviceUserName,
                                customerUserName=customerUserName,
                                req=req,
                                form=form,
                                appointment_date=appointment_date,
                                completion_date=completion_date,
                                **nav_data)
    

def professionalRequestSView(serviceUserName,customerUserName,req):
    if req == 'makeascomleted':
        res = make_it_completed(serviceUserName,customerUserName)
        if not res:
            return ApiError.internal_server_error('Unable to make service completed')
        return redirect(url_for('professional_route_view', userName=serviceUserName))
    elif req == 'makeitunavailable' and customerUserName=='none':
        makeServiceAvailabiltyChange(serviceUserName)
        return redirect(url_for('professional_profile_route_view', userName=serviceUserName))
    elif req == 'makeitavailable' and customerUserName=='none':
        makeServiceAvailabiltyChange(serviceUserName)
        return redirect(url_for('professional_profile_route_view', userName=serviceUserName))

    return {'error':'Invalid Request'}