#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pkg import limits as lim     #lim dependency
from werkzeug.security import generate_password_hash

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a
import pkg.fsqlite as sq #extra for any db commits
from pkg.servlog import srvlog,logtofile

bp = Blueprint('dataview', __name__, url_prefix='/admintools')

@bp.route('/busadd',methods=['GET','POST'])
@a.admin_required
def busadd():
    '''adds a system user onto the system'''
    busadd_form = fm.Bus_Driver_RegisterForm()
    if busadd_form.validate_on_submit():
        target_user = md.Bus_Driver.query.filter(md.Bus_Driver.busname == busadd_form.busname.data).first()
        if(target_user == None):
            hpass = generate_password_hash(busadd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
            target_add = md.Bus_Driver(busadd_form.busname.data,hpass)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            #srvlog["sys"].info(busadd_form.busname.data+" registered as new user) #logging
            return render_template("message.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
                busname=current_user.username,
                display_title="Success",
                display_message="Added "+target_add.busname+" into the system.")

        else:
            return render_template("error.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            Busname=current_user.busname,
            error_title="Failure",
            error_message="Busname already exists!")

    return render_template('busadd.html',form=busadd_form)

@bp.route('/bus_view',methods=['GET','POST'])
def buslist():
#    '''list out system bus'''
#    busview_form = fm.Data_ViewForm()
#    return render_template('/buslist.html',form=busview_form)
    '''list out bus users'''
    columnHead = ["busname"]
    buslist = md.Bus_Driver.query.all()
    match = []
    for users in buslist:
        temp = [users.busname]
        match.append(temp)
    return render_template('buslist.html',PAGE_MAIN_TITLE=const.SERVER_NAME,
        colNum=len(columnHead),matches=match,columnHead=columnHead)

@bp.route('/busadd',methods=['GET','POST'])

def busadd_nologin():#This function is for initial server initialization only,
	#NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''Adds a bus into system using admintools, no checking is done
    Use only in initial deployment phase, please switch off the routes
    regarding this one it is done. returns 0 on success and 1 on fail'''
    busadd_form = fm.Bus_Driver_RegisterForm()
    if busadd_form.validate_on_submit():
        hpass = generate_password_hash(busadd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
        target_add = md.Bus_Driver(busadd_form.busname.data,hpass)#create user obj
        sq.db_session.add(target_add)#adds user object onto database.
        sq.db_session.commit()
    return render_template('busadd.html',form=busadd_form)

@bp.route('/busmod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def busmod(primaryKey):
    '''modify system user'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.Bus_Driver.query.filter(md.Bus_Driver.busname == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" deleted from the system") #logging
            return redirect(url_for('dataview.buslist'))
