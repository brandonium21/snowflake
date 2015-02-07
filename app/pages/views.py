# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import render_template
from flask_user import login_required, roles_required
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from app.app_and_db import app, db
from flask import redirect, render_template, render_template_string, get_template_attribute

# The Home page is accessible to anyone
@app.route('/snowflake')
def home_page():
    return render_template('pages/home_page.html')

# The Member page is accessible to authenticated users (users that have logged in)
@app.route('/member')
@login_required             # Limits access to authenticated users
def member_page():
    return redirect(url_for('testPage'))

# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')

