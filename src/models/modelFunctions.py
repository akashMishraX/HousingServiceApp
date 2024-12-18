import datetime
from ..utils.helperErrorHandler import ApiError
from ..models.model import *

def createAdmin():
    #creating dummy admin 
    role = RoleType.query.filter_by(name='Admin').first()
    user_instance = User(username = 'admin',
                        password = '99999',
                        email = 'admin@123gmail.com',
                        phoneNumber = '3333333333',
                        roleId = role.id)
    db.session.add(user_instance)
    db.session.commit()
    address_instance = UserAddress(city = '',
                    state = '',
                    country = '',
                    postalCode ='',
                    addressDescription = '',
                    userId = user_instance.id)
    db.session.add_all([address_instance])
    db.session.commit()


def create_customer(data):
    role = RoleType.query.filter_by(name='Customer').first()
    user_instance = User(username = data['username'],
                        password = data['password'],
                        email = data['email'],
                        phoneNumber = data['phone_number'],
                        roleId = role.id)
    db.session.add(user_instance)
    db.session.commit()
    print(user_instance.id)
    address_instance = UserAddress(city = data['city'],
                                state = data['state'],
                                country = data['country'],
                                postalCode = data['postal_code'],
                                addressDescription = data['address_description'],
                                userId = user_instance.id)
    customer_instance = Customer(id = user_instance.id)

    db.session.add_all([address_instance,customer_instance])
    db.session.commit()

def create_service_professional(data):
    role = RoleType.query.filter_by(name='ServiceProfessional').first()
    user_instance = User(username = data['username'],
                        password = data['password'],
                        email = data['email'],
                        phoneNumber = data['phone_number'],
                        roleId = role.id)
    db.session.add(user_instance)
    db.session.commit()
    
    address_instance = UserAddress(city = data['city'],
                                state = data['state'],
                                country = data['country'],
                                postalCode = data['postal_code'],
                                addressDescription = data['address_description'],
                                userId = user_instance.id)
    category_instance = Category.query.filter_by(name=data['category'].capitalize()).first()
    service_professional_instance = ServiceProfessional(id = user_instance.id,
                                                        categoryId = category_instance.id,
                                                        serviceName = data['service_name'],
                                                        description = data['description'])
                                                        

    db.session.add_all([address_instance,service_professional_instance])
    db.session.commit()

def request_service(data,action):
    if action == 'book':
        customer = User.query.filter_by(username=data['customerUserName']).first()
        service = User.query.filter_by(username=data['serviceUserName']).first()
        expected_date = datetime.datetime.strptime(data['expected_date'], "%Y-%m-%d").date()
        
        old_sr = ServiceRequested.query.filter_by(customerId=customer.id , serviceProfessionalId=service.id).all()
        for s in old_sr:
            if s.serviceStatus.value == 'Pending':
                return False
            if s.serviceStatus.value == 'Accepted':
                asP = AssignedService.query.filter_by(id=s.id).first()
                if asP.workStatus.value == 'Pending':
                    return False


        sr = ServiceRequested(expectedDate = expected_date ,
                                serviceStatus = 'Pending',
                                customerId = customer.id,
                                serviceProfessionalId = service.id)

        db.session.add(sr)
        db.session.commit()
    if action == 'edit':
        customer = User.query.filter_by(username=data['customerUserName']).first()
        service = User.query.filter_by(username=data['serviceUserName']).first()
        sr = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,customerId=customer.id,serviceStatus='Pending').first()
        sr.expectedDate = datetime.datetime.strptime(data['expected_date'], "%Y-%m-%d").date()
        db.session.commit()
    return True

def make_it_rejected(serviceUserName,customerUserName):
    customer = User.query.filter_by(username=customerUserName).first()
    service = User.query.filter_by(username=serviceUserName).first()
    sr = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,customerId=customer.id,serviceStatus='Pending').all()
    for s in sr:
        s.serviceStatus = 'Rejected'
    db.session.commit()
    return True

def make_it_accepted(serviceUserName,customerUserName,appoinment_date,completion_date):
    customer = User.query.filter_by(username=customerUserName).first()
    service = User.query.filter_by(username=serviceUserName).first()


    # Logic for rejected request
    sr = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,customerId=customer.id).all()
    my_sr =''
    for s in sr:
        if s.serviceStatus.value == 'Pending':
            s.serviceStatus = 'Accepted'
            my_sr = s

    appoinmentOn = datetime.datetime.strptime(appoinment_date, "%Y-%m-%d").date()
    completionOn = datetime.datetime.strptime(completion_date, "%Y-%m-%d").date()
    aS = AssignedService.query.filter_by(id=my_sr.id).all()
    if len(aS) != 0:
        return False
    assignedService = AssignedService(
        appointmentDate = appoinmentOn,
        completionDate = completionOn,
        workStatus = 'Pending',
        id = my_sr.id
    ) 
    db.session.add(assignedService)
    db.session.commit()
    return True

def make_it_completed(serviceUserName,customerUserName):
    customer = User.query.filter_by(username=customerUserName).first()
    service = User.query.filter_by(username=serviceUserName).first()
    sr = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,customerId=customer.id,serviceStatus='Accepted').all()
    for s in sr:
        aS = AssignedService.query.filter_by(id=s.id,workStatus='Pending').first()
        if aS is None:continue
        aS.workStatus = 'Completed'
    db.session.commit()
    return True


def cancel_appointment(customerUserName,serviceUserName):
    print(customerUserName,serviceUserName)
    customer = User.query.filter_by(username=customerUserName).first()
    service = User.query.filter_by(username=serviceUserName).first()
    sr = ServiceRequested.query.filter_by(serviceProfessionalId=service.id,customerId=customer.id,serviceStatus='Accepted').all()
    print(sr)
    for s in sr:
        aS = AssignedService.query.filter_by(id=s.id,workStatus='Pending').first()
        print(aS)
        if aS is None:continue
        aS.workStatus = 'Canceled'
    db.session.commit()
    return True

def makeServiceAvailabiltyChange(serviceUserName):
    service = User.query.filter_by(username=serviceUserName).first()
    serviceP = ServiceProfessional.query.filter_by(id=service.id).first()
    if serviceP.isAvailable == True:
        serviceP.isAvailable = False
    else:
        serviceP.isAvailable = True
    db.session.commit()
    return True

def changeServiceApproval(id):
    serviceP = ServiceProfessional.query.filter_by(id=id).first()
    if serviceP.isApproved == True:
        serviceP.isApproved = False
    else:
        serviceP.isApproved = True
    db.session.commit()
    return True

def addCategory(name,pricing,time_required):
    category = Category.query.filter_by(name=name).first()
    if category is None:
        category = Category(name=name,pricing=pricing,timeRequired=time_required)
        db.session.add(category)
        db.session.commit()
        return True
    return False

def editCategory(name,pricing,time_required,id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return False
    category.name = name
    category.pricing = pricing
    category.timeRequired = time_required
    db.session.commit()
    return True

def changeCustomerFlag(id):
    customer = Customer.query.filter_by(id=id).first()

    if customer.isFlagged == True:
        customer.isFlagged = False
    else:
        customer.isFlagged = True
    db.session.commit()
    return True

def addRating(requestId,rating,feedback):
    aS = AssignedService.query.filter_by(id=requestId).first()
    print(aS,rating,feedback)
    aS.rating = rating
    aS.feedback = feedback
    db.session.commit()
    return True

def updateRating(id,rated):
    serviceP = ServiceProfessional.query.filter_by(id=id).first()
    RATED =  round(rated, 2)
    serviceP.serviceRating = RATED
    db.session.commit()
    return True