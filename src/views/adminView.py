from flask import jsonify, redirect, render_template, request, url_for

from ..forms.searchServiceProfessional import SearchProfessionalForm

from ..utils.helperErrorHandler import ApiError

from ..models.modelFunctions import addCategory, changeCustomerFlag, changeServiceApproval, editCategory

from ..forms.createCategory import CreateCategory, EditCategory
from ..routers._layout import BASE_URL

from ..models.model import AssignedService, Category, Customer, ServiceProfessional, ServiceRequested, User

def AdminHomeView(userName):
    customer = Customer.query.filter_by().all()
    serviceP = ServiceProfessional.query.filter_by().all()
    nav_data = {
        'page_title': 'Admin',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Service', 'url': url_for('admin_service_route_view', userName=userName), 'active': True},
            {'text': 'Customer', 'url': url_for('admin_customer_route_view', userName=userName,action='view',id=0), 'active': True},
            {'text':'Search','url':url_for('admin_search_route_view',userName=userName,action='view',id=0),'active':True}
        ],
        'customer_count':len(customer),
        'service_count':len(serviceP),
        'logout': True,
    }
    return render_template('admin/home.html',userName=userName,**nav_data)

def AdminServiceView(userName):
    all_services = []
    serviceP = ServiceProfessional.query.filter_by().all()
    for service in serviceP:
        category = Category.query.filter_by(id=service.categoryId).first()
        serviceUser = User.query.filter_by(id=service.id).first()
        serviceR = ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()
        lenCancelled = 0
        lenCompleted = 0
        for s in serviceR:
            aS = AssignedService.query.filter_by(id=s.id).first()
            if aS is None:continue
            if aS.workStatus.value == 'Completed':
                lenCompleted += 1
            if aS.workStatus.value == 'Canceled':
                lenCancelled += 1
        obj = {
            'info':{
                'id':service.id,
                'name':service.serviceName,
                'username':serviceUser.username,
                'email':serviceUser.email,
                'phone':serviceUser.phoneNumber,
                'address':f'{serviceUser.address.city}, {serviceUser.address.state}, {serviceUser.address.country}',
                'category':category.name,
                'price':category.pricing
            },
            'isApproved':service.isApproved,
            'isAvailable':service.isAvailable,
            'work_stats':{
                'total':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()),
                'pending':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Pending').all()),
                'rejected':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Rejected').all()),
                'completed':lenCompleted,
                'cancelled':lenCancelled,
                'rating':service.serviceRating
            },
        }
        all_services.append(obj)

    all_category=[]
    categories = Category.query.filter_by().all()
    for category in categories:
        serviceP = ServiceProfessional.query.filter_by(categoryId=category.id).all()
        obj={
            'name':category.name,
            'pricing':category.pricing,
            'time_required':category.timeRequired,
            'services_count':len(serviceP),
            'catgeory_id':category.id
        }
        all_category.append(obj)


    nav_data = {
        'page_title': 'Admin',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('admin_route_view', userName=userName), 'active': True},
            {'text': 'Customer', 'url': url_for('admin_customer_route_view', userName=userName,action='view',id=0), 'active': True},
            {'text':'Search','url':url_for('admin_search_route_view',userName=userName,action='view',id=0),'active':True}
        ],
        'logout': True,
        'all_services':all_services,
        'all_category':all_category
    }
    return render_template('admin/service.html',userName=userName,**nav_data)

def AdminCustomerView(userName,action,id):
    if action == 'changeCustomerFlag':
        changeCustomerFlag(id)
        return redirect(url_for('admin_customer_route_view', userName=userName,action='view',id=0))
    customers = Customer.query.filter_by().all()
    all_customer = []
    for customer in customers:
        serviceR  = ServiceRequested.query.filter_by(customerId=customer.id,serviceStatus='Accepted').all()
        total_service_taken = 0
        money_spend = 0
        for s in serviceR:
            aS = AssignedService.query.filter_by(id=s.id,workStatus='Completed').first()
            if aS is None:continue
            serviceP = ServiceProfessional.query.filter_by(id=s.serviceProfessionalId).first()
            category = Category.query.filter_by(id=serviceP.categoryId).first()
            total_service_taken +=  1
            money_spend += category.pricing
        customerUser  = User.query.filter_by(id=customer.id).first()
        obj = {
            'info':{
                'id':customerUser.id,
                'username':customerUser.username,
                'email':customerUser.email,
                'phone':customerUser.phoneNumber,
                'address':f'{customerUser.address.city}, {customerUser.address.state}, {customerUser.address.country}',
            },
            'isFlagged':customer.isFlagged,
            'total_service_taken':total_service_taken,
            'money_spend':money_spend
        }
        all_customer.append(obj)
    nav_data = {
        'page_title': 'Admin',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('admin_route_view', userName=userName), 'active': True},
            {'text': 'Service', 'url': url_for('admin_service_route_view', userName=userName), 'active': True},    
            {'text':'Search','url':url_for('admin_search_route_view',userName=userName,action='view',id=0),'active':True} 
        ],
        'logout': True,
        'all_customer':all_customer
    }
    return render_template('admin/customer.html',userName=userName,**nav_data)

def AdminCategoryView(userName,action,id):
    previous_url = request.referrer or BASE_URL
    
    if action == 'create':
        nav_data = {
        'page_title': 'Create Category',
        'site_title': {'name': '', 'url': '', 'active': False},
        'nav_items': [
            {'text': '< Back', 'url': previous_url,'active': True},
        ],
        'logout': True,
        'form_data':{
            'title': 'Create Category',
        }
        }
        if request.method == 'POST':
            res = addCategory(request.form['name'],request.form['pricing'],request.form['time_required'])
            if res == False:
                return ApiError.internal_server_error('Category already exists')
            return redirect(url_for('admin_service_route_view', userName=userName))
        
        name = pricing = time_required= ''
        form = CreateCategory()
        if form.validate_on_submit():
            name = form.name.data
            pricing = form.pricing.data
            time_required = form.time_required.data

    elif action == 'edit':
        nav_data = {
        'page_title': 'Edit Category',
        'site_title': {'name': '', 'url': '', 'active': False},
        'nav_items': [
            {'text': '< Back', 'url': previous_url,'active': True},
        ],
        'logout': True,
        'form_data':{
            'title': 'Edit Category',
        }
        }

        if request.method == 'POST':
            res = editCategory(request.form['name'],request.form['pricing'],request.form['time_required'],id)
            if res == False:
                return ApiError.internal_server_error('Category does not exists')
            return redirect(url_for('admin_service_route_view', userName=userName))

        categoryData = Category.query.filter_by(id=id).first()
        if categoryData:
            name = categoryData.name
            pricing = categoryData.pricing
            time_required = categoryData.timeRequired
            form = EditCategory(name=name,pricing=pricing,time_required=time_required)
            if form.validate_on_submit():
                name = form.name.data
                pricing = form.pricing.data
                time_required = form.time_required.data
        else:
            return ApiError.internal_server_error('Category not found')
        
        
    elif action == 'changeServiceApprovalForService':
        changeServiceApproval(id)
        return redirect(url_for('admin_service_route_view', userName=userName))
    elif action == 'changeServiceApprovalForSearch':
        changeServiceApproval(id)
        return redirect(url_for('admin_search_route_view', userName=userName,action='view',id=0))
    
    return render_template('admin/create_category.html',
                           userName=userName,
                           form=form,
                           name=name,
                           pricing=pricing,
                           time_required=time_required,
                           **nav_data)

def AdminSearchView(userName,action,id):
    
    nav_data = {
        'page_title': 'Admin',
        'site_title': {'name': f'{userName}', 'url': '', 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': url_for('admin_route_view', userName=userName), 'active': True},
            {'text': 'Service', 'url': url_for('admin_service_route_view', userName=userName), 'active': True},  
            {'text': 'Customer', 'url': url_for('admin_customer_route_view', userName=userName,action='view',id=0), 'active': True},   
        ],
        'logout': True,
    }
    input = search_by = ''
    form = SearchProfessionalForm()
    if form.validate_on_submit():
        input = form.input.data
        search_by = form.search_by.data

    all_services = []
    if request.method == 'POST': 
        if search_by == 'username':
            serviceUser = User.query.filter_by(username=input).first()
            if serviceUser is None:
                return ApiError.bad_request('No Such User Found')
            service = ServiceProfessional.query.filter_by(id=serviceUser.id).first()
            category = Category.query.filter_by(id=service.categoryId).first()

            serviceUser = User.query.filter_by(id=service.id).first()
            serviceR = ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()
            lenCancelled = 0
            lenCompleted = 0
            for s in serviceR:
                aS = AssignedService.query.filter_by(id=s.id).first()
                if aS.workStatus.value == 'Completed':
                    lenCompleted += 1
                if aS.workStatus.value == 'Canceled':
                    lenCancelled += 1
 
            obj = {
                'info':{
                    'id':service.id,
                    'name':service.serviceName,
                    'username':serviceUser.username,
                    'email':serviceUser.email,
                    'phone':serviceUser.phoneNumber,
                    'address':f'{serviceUser.address.city}, {serviceUser.address.state}, {serviceUser.address.country}',
                    'category':category.name,
                    'price':category.pricing
                },
                'isApproved':service.isApproved,
                'isAvailable':service.isAvailable,
                'work_stats':{
                    'total':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()),
                    'pending':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Pending').all()),
                    'rejected':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Rejected').all()),
                    'completed':lenCompleted,
                    'cancelled':lenCancelled,
                    'rating':service.serviceRating
                },
            }
            all_services.append(obj)

        elif search_by == 'category':
            category = Category.query.filter_by(name=input).first()
            if category is None:
                return ApiError.bad_request('No Such Category Found')
            serviceP = ServiceProfessional.query.filter_by(categoryId=category.id).all()
            for service in serviceP:
                category = Category.query.filter_by(id=service.categoryId).first()
                serviceUser = User.query.filter_by(id=service.id).first()
                serviceR = ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()
                lenCancelled = 0
                lenCompleted = 0
                for s in serviceR:
                    aS = AssignedService.query.filter_by(id=s.id).first()
                    if aS.workStatus.value == 'Completed':
                        lenCompleted += 1
                    if aS.workStatus.value == 'Canceled':
                        lenCancelled += 1
                print(lenCompleted,lenCancelled)
                obj = {
                    'info':{
                        'id':service.id,
                        'name':service.serviceName,
                        'username':serviceUser.username,
                        'email':serviceUser.email,
                        'phone':serviceUser.phoneNumber,
                        'address':f'{serviceUser.address.city}, {serviceUser.address.state}, {serviceUser.address.country}',
                        'category':category.name,
                        'price':category.pricing
                    },
                    'isApproved':service.isApproved,
                    'isAvailable':service.isAvailable,
                    'work_stats':{
                        'total':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id).all()),
                        'pending':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Pending').all()),
                        'rejected':len(ServiceRequested.query.filter_by(serviceProfessionalId=service.id,serviceStatus='Rejected').all()),
                        'completed':lenCompleted,
                        'cancelled':lenCancelled,
                        'rating':service.serviceRating
                    },
                }
                all_services.append(obj)


    return render_template('admin/search.html',
                           userName=userName,
                           form=form,
                           input=input,
                           search_by=search_by,
                           all_services=all_services,
                           **nav_data)