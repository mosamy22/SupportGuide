from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from dbconfig import Server,Base
from sqlalchemy.orm import sessionmaker,joinedload
from flask import make_response
from flask import session as login_session
import random
import string
from flask_httpauth import HTTPBasicAuth
import httplib2
import json
import requests

auth = HTTPBasicAuth()
app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///guide.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#main page
@app.route('/')
def MainPage():
    return render_template('ebc.html')

#login page
# Create anti-forgery state token
@app.route('/login' , methods=['GET', 'POST'])
def ShowLogin():
    if request.method == 'POST':
        if request.form['username'] == 'sysadmin' and request.form['password'] == 'P@ssw0rd':
            state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                            for x in xrange(32))
            login_session['state'] = state
            login_session['username'] = 'sysadmin'
            return redirect(url_for('ShowServers'))
        else :
            error = "Invalid Username or password "
            return render_template('login.html',invalid_user = error)

    # return "The current session state is %s" % login_session['state']
    return render_template('login.html')

#@auth.login_required
@app.route('/applications/')
def ShowServers():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    apps = session.query(Server)
    if 'username' not in login_session:
        return render_template('ebc.html')
    #else:
    return render_template('server.html', apps=apps)

# show the Application details
@app.route('/applications/<string:project_name>')
def ShowAppDetails(project_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    app = session.query(Server).filter_by(project = project_name).one()
    return render_template('description.html', app = app)

# Edit the project
@app.route('/applications/<string:project_name>/edit/', methods=['GET', 'POST'])
def EditApp(project_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedApp = session.query(Server).filter_by(project=project_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['description']:
            editedApp.description = request.form['description']
        if request.form['pAppServer']:
            editedApp.app_prod_ip = request.form['pAppServer']
        if request.form['pDbServer']:
            editedApp.db_prod_ip = request.form['pDbServer']
        if request.form['sAppServer']:
            editedApp.app_stage_ip = request.form['sAppServer']
        if request.form['sDbServer']:
            editedApp.db_stage_ip = request.form['sDbServer']
            session.add(editedApp)
            session.commit()
            return redirect(url_for('ShowAppDetails',project_name = editedApp.project))
    else:
        return render_template('editproj.html', app=editedApp)

# Create a new App

@app.route('/applications/new/', methods=['GET', 'POST'])
def newApp():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['project'] and request.form['description'] and request.form['pAppServer'] and request.form['pDbServer'] and request.form['sAppServer'] and request.form['sDbServer']:
            newApp = Server(
                project=request.form['project'],description=request.form['description'],app_prod_ip = request.form['pAppServer'],app_stage_ip = request.form['sAppServer'],db_prod_ip = request.form['pDbServer'],db_stage_ip = request.form['sDbServer'])
            session.add(newApp)
            session.commit()
            return redirect(url_for('ShowServers'))
        else :
            return "<script>function myFunction() {alert('You must insert all mandatory feilds');}</script><body onload='myFunction()'>"
    else:
        return render_template('addproj.html')

# Delete the App
@app.route('/applications/<string:project_name>/delete/', methods=['GET', 'POST'])
def deleteApp(project_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    deletedApp = session.query(Server).filter_by(project=project_name).one()
    if request.method == 'POST':
        session.delete(deletedApp)
        session.commit()
        return redirect(url_for('ShowServers'))
    else:
        return render_template('deleteApp.html', app= deletedApp)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
