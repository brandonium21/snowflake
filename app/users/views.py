# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string
from flask import request, url_for
from app.app_and_db import app, db
from app.users.forms import UserProfileForm
from flask_user import current_user, login_required, roles_required
from flask import request
from flask import json
from models import *
import re
#
# User Profile form
#
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method=='POST' and form.validate():

        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('users/user_profile_page.html',
        form=form)

@app.route('/delete', methods=['GET', 'POST'])
@login_required             # Limits access to authenticated users
def delete():
    if request.method == 'POST':
        id_get = request.form['delete']
        id_row = Url.query.get(id_get)
        db.session.delete(id_row)
        db.session.commit()
        user_id = current_user.id
        links = Url.query.filter_by(user_id = user_id).all()
        uniqueID = UserAuth.query.filter_by(user_id = user_id).first()

        return redirect(url_for('testPage'))
    return redirect(url_for('testPage'))

@app.route('/letitsnow', methods=['GET', 'POST'])
@login_required             # Limits access to authenticated users
def testPage():
    user_id = current_user.id
    links = Url.query.filter_by(user_id = user_id).all()
    uniqueID = UserAuth.query.filter_by(user_id = user_id).first()      
    if request.method == 'POST':
        #clicks = 0
            title = request.form['title']
            url = request.form['url']
            if url.startswith('http://') or url.startswith('https://'):
                url = url
            else:
                url = 'http://' + url
            description = request.form['description']
            data = Url(title, url, description, user_id)
            db.session.add(data)
            db.session.commit()
            links = Url.query.filter_by(user_id = user_id).all()
    print 'worked'
    return render_template('pages/letitsnow.html', links= links, user = uniqueID)


@app.route('/<username>', methods=['GET', 'POST'])
def show(username):
    #user_id
    userID = UserAuth.query.filter_by(username = username).first()
    #links
    links = Url.query.filter_by(user_id = userID.user_id).all()

    print links
    return render_template('pages/show.html', user = username, links = links)

@app.route('/', methods=['GET', 'POST'])
def alt_home():
    return render_template('pages/home_page.html')
'''
@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():

    if request.method == 'POST':
        url = request.form['url']
        clicked = Url.query.filter_by(url = url).first()
        clicked  
    return render_template('pages/stats.html', user = username, links = links, stats=stats)
'''

@app.route('/log', methods= ['GET', 'POST'])
@roles_required('admin')
def log():
    users = UserAuth.query.all()
    url = Url.query.all()
    print users
    print url
    return render_template("pages/log.html", users= users )
    return 'none'

################### SIMPLE WAKE-UP ##############################

@app.route('/snowflake/wakeup', methods=['GET'])
def wakeup():
    return 'im awake'

#################################################################

@app.errorhandler(500)
def page_not_found(e):
    return render_template('pages/404.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404
