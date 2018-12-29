#--------------------------------------------------
# admintools.py
# this file contains functions and routes
# for admin usage
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint
from pkg import limits as lim

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a
import pkg.fsqlite as sq #extra for any db commits
from pkg.servlog import srvlog,logtofile

#additional overheads
import os

bp = Blueprint('Bus_Driver_Data', __name__, url_prefix='/admintools')

##############################################################################################
# system user add/mod routes
# USER ADD ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/bus_add',methods=['GET','POST'])
@a.admin_required
def bus_add():
    '''adds a system user onto the system'''
    bus_add_form = fm.Driver_RegisterForm()
    if bus_add_form.validate_on_submit():
        driver_add = md.Driver_Register.query.filter(md.Driver_Register.username == bus_add_form.username.data).first()
        if(driver_add == None):
            hpass = generate_password_hash(bus_add_form.Dpassword.data,method=const.HASH_ALGORITHM_0)#password hashing
            driver_addd = md.Driver_Register(bus_add_form.username.data,bus_add_form.Drivername.data,bus_add_form.Dexperience.data,hpass)#create user obj
            sq.db_session.add(driver_addd)#adds user object onto database.
            sq.db_session.commit()
            #srvlog["sys"].info(bus_add_form.Drivername.data+" registered as new driver, Driver="+str(bus_add_form.adminPriv.data)) #logging
            return render_template("message.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
                username=current_user.username,
                Drivername=driver_addd.Drivername,
                Dexperience=driver_addd.Dexperience,
                display_title="Success",
                display_message="Added "+driver_addd.Drivername+" into the system.")

        else:
            return render_template("error.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            username=current_user.username,
            error_title="Failure",
            error_message="Driver username already exists!")

    return render_template('bus_add.html',form=bus_add_form)

##############################################################################################
# USER LIST ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/bus_list',methods=['GET','POST'])
@a.admin_required
def bus_list():
    '''list out system users'''
    columnHead = ["Drivername"]
    bus_list = md.Driver_Register.query.all()
    match = []
    for users in bus_list:
        temp = [users.Drivername]
        match.append(temp)
    return render_template('bus_list.html',PAGE_MAIN_TITLE=const.SERVER_NAME,
        colNum=len(columnHead),matches=match,columnHead=columnHead)

@bp.route('/bus_add',methods=['GET','POST'])
##############################################################################################
# USER MODIFY ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
def bus_add_nologin():
     bus_add_form = fm.Bus_Driver_RegisterForm()
     if busadd_form.validate_on_submit():
        hpass = generate_password_hash(busadd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
        target_add = md.Bus_Driver(busadd_form.busname.data,hpass)#create user obj
        sq.db_session.add(target_add)#adds user object onto database.
        sq.db_session.commit()
        return render_template('busadd.html',form=busadd_form)
    #    elif(request.form["button"]=="Modify"):
    #        usermod_form = fm.System_User_EditForm()
    #        usermod_form.adminPriv.default = ('1' if adminpri else '0')
    #        usermod_form.process()
    #        return render_template("usermod.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
    #        primaryKey=primaryKey,form = usermod_form)

    #    elif(request.form["button"]=="Submit Changes"):
    #        adminpri = request.form.get("adminPriv")
    #        target_mod = md.System_User.query.filter(md.System_User.username == primaryKey).first()
    #        target_mod.adminpri = True if adminpri == '1' else False
    #        sq.db_session.add(target_mod)
    #        sq.db_session.commit()
    #        return redirect(url_for('admintools.userlist',username=current_user.username))

    #    else:
    #        abort(404)

    #else:
    #    abort(400)

##############################################################################################
# nologin routes (requires no login) PLEASE REFRAIN IN ACTUAL DEPLOYMENT SERVERS
##############################################################################################
@bp.route('/driver_mod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def driver_mod(primaryKey):
    '''modify system user'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.Driver_Register.query.filter(md.Driver_Register.username == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" deleted from the system") #logging
            return redirect(url_for('Bus_Driver_Data.bus_list'))

        elif(request.form["button"]=="Modify"):
            drivermod_form = fm.Driver_RegisterForm()
            drivermod_form.process()
            return render_template("bus_mod.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            primaryKey=primaryKey,form = drivermod_form)

        elif(request.form["button"]=="Submit Changes"):
            target_mod = md.Driver_Register.query.filter(md.Driver_Register.username == primaryKey).first()
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('Bus_Driver_Data.bus_list',username=current_user.username))

        else:
            abort(404)

    else:
        abort(400)
##############################################################################################
# Logging routes (display server logs)
# ported from old pyflask project : update2
##############################################################################################
#@bp.route('/logs/<logtype>')
#@a.admin_required
#def logview(logtype):
    #Display logs on the local server
#    filebuff = []
#    with open( os.path.join(const.LOGS_DIR,logtofile[logtype]) ,'r' ) as f:
        #opens the logfile of required logtype for reading
#        for line in f:
#            filebuff.append(line)
#        if(len(filebuff) == 0):
#            filebuff = ["Empty, No logs at the moment"]
#        return render_template("admintools/logging.html",
#                            	PAGE_MAIN_TITLE=const.SERVER_NAME,
#                            	logfile = filebuff)
