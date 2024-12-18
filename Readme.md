# Home Service Management App

## Abstract➖

The Home Service Management System aims to create a platform that connects services
professions with customer seeking home services.This system allows booking feature,
rating feature ,multi-role feature ,search feature and category feature with implementation
of CRUD with REST architecture.

## Approach➖

    System Architecture:-
    ❖ Used Flask as a backend server with SQLite as Database
    ❖ Implemented RestFul architecture
    ❖ Created a config.py for handling production based configuration
    ❖ Properly distributed Point of concern based on structure.

    Database Design:-
    ❖ Created a schema using Flask-SQLAlchemy ORM
    ❖ Designed Tables to handle incoming requests(“ServiceRequested”) and
    Accepted requests (“AssignedService”).➖
    ❖ Created “User” as the primary parent for where other users derived.

## Technical Stack➖
    Backend:- Flask , Sqlite, Flask-sqlalchemy
    View:- Html 5 ,CSS 3 ,BootStrap v5 , Jinja
    Validation :- Flask Wtforms
    Database viewer :- SQlite3 Editor Vscode extension
## Database schema
    Schema :-➖Mad1-proj-schema-design.png

## Key Implementation:-
    ❖ User Management:-
        Admin:-
            ➢ Admin can flag/unflag a customer and block/unblock a service
        profession
            ➢ Admin can create new categories of services.
        ❖ Service Management:-
            ➢ Service professionals can Accept/Reject a service request
            ➢ Service professionals can Create Appointments and Complete it after
        completion.
        ❖ Customer Management:-
            ➢ Customers can search for a service and book/edit/cancel services.
            ➢ Customers can rate and give feedback for a service after its completion.
Video link :-mad1-project-live-demo.mp4
