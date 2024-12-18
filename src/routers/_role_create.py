from flask import current_app as app, jsonify, redirect, render_template, request

from ..models.modelFunctions import createAdmin
from ..models.model import *
from src.routers._layout import *


# This is complete internel route need refactiring later

@app.route('/create_role',methods=['GET','POST'])
def role_create():
    nav_data = {
        'page_title': 'Create Role',
        'site_title': {'name': 'The Home Team', 'url': BASE_URL, 'active': True},
        'nav_items': [],
        'logout': False
    }
    if request.method == 'POST':
        roles= [
                { 'role_name': "Admin" },
                { 'role_name': "Customer" },
                { 'role_name': "ServiceProfessional" }
            ]
        # return f'{roles[0]}'
        try:
            
            for role in roles:
                role = RoleType(name=role['role_name'])
                db.session.add(role)
            db.session.commit()
            createAdmin()
            return redirect(BASE_URL)
        except Exception as e:
            return jsonify({"message": f"Error: {e}", "roles": []})



    return render_template('_create_role.html',**nav_data)