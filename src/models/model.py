from flask_sqlalchemy import SQLAlchemy
from enum import Enum
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(25),nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String(25),unique=True, nullable=False)
    phoneNumber  = db.Column(db.String(15), nullable=False)

    roleId  = db.Column(db.Integer, db.ForeignKey('role_type.id'),nullable=False)
    address = db.relationship('UserAddress',uselist=False,backref='user')
    customer = db.relationship('Customer',uselist=False,backref='user')
    serviceProfessional = db.relationship('ServiceProfessional',uselist=False,backref='user')


class role_type_enum(Enum):
    Admin = 'Admin'
    Customer = 'Customer'
    ServiceProfessional = 'ServiceProfessional'
class RoleType(db.Model):
    __tablename__ = 'role_type'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Enum(role_type_enum),nullable=False,unique=True)


class UserAddress(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(25), nullable=False)
    postalCode = db.Column(db.String(25), nullable=False)
    addressDescription = db.Column(db.String(50), nullable=False)


class Customer(db.Model):
    __tablename__ = 'customer'
    # id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    isFlagged = db.Column(db.Boolean, nullable=False,default=False)
    
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(25),nullable=False,unique=True)
    pricing = db.Column(db.Integer, nullable=False)
    timeRequired = db.Column(db.Integer, nullable=False)

class ServiceProfessional(db.Model):
    __tablename__ = 'service_professional'
    # id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    id  = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    isApproved = db.Column(db.Boolean, nullable=False,default=False)
    isAvailable =  db.Column(db.Boolean, nullable=False,default=False)
    categoryId =  db.Column(db.Integer, db.ForeignKey('category.id'))
    serviceName = db.Column(db.String(25), nullable=False)
    description =  db.Column(db.String(25), nullable=False)
    serviceRating = db.Column(db.Float, nullable=False ,default=0)
    experience = db.Column(db.Integer, nullable=False ,default=0)


class service_requested_status(Enum):
    Pending = 'Pending'
    Accepted = 'Accepted'
    Rejected = 'Rejected'
class ServiceRequested(db.Model):
    __tablename__ = 'service_requested'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    serviceStatus = db.Column(db.Enum(service_requested_status),nullable=False)
    expectedDate = db.Column(db.DateTime,nullable=False)
   

    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'),nullable=False)
    serviceProfessionalId = db.Column(db.Integer, db.ForeignKey('service_professional.id'),nullable=False)
    


class service_rating(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
class work_status_enum(Enum):
    Pending = 'Pending'
    Completed = 'Completed'
    Canceled = 'Canceled'
class AssignedService(db.Model):
    __tablename__ = 'assigned_service'
    id = db.Column(db.Integer,db.ForeignKey('service_requested.id'),primary_key=True)
    appointmentDate = db.Column(db.DateTime,nullable=False)
    completionDate = db.Column(db.DateTime)
    workStatus = db.Column(db.Enum(work_status_enum),nullable=False)
    rating = db.Column(db.Enum(service_rating))
    feedback = db.Column(db.String(25))
   