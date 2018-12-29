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

bp = Blueprint('admintools', __name__, url_prefix='/admintools')

##############################################################################################
# system user add/mod routes
# USER ADD ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/useradd',methods=['GET','POST'])
@a.admin_required
def useradd():
    '''adds a system user onto the system'''
    useradd_form = fm.System_User_RegisterForm()
    if useradd_form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.username == useradd_form.username.data).first()
        if(target_user == None):
            hpass = generate_password_hash(useradd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
            target_add = md.System_User(useradd_form.username.data,hpass,True if int(useradd_form.adminPriv.data) else False)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            srvlog["sys"].info(useradd_form.username.data+" registered as new user, admin="+str(useradd_form.adminPriv.data)) #logging
            return render_template("standard/message.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
                username=current_user.username,
                display_title="Success",
                display_message="Added "+target_add.username+" into the system.")

        else:
            return render_template("errors/error.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            username=current_user.username,
            error_title="Failure",
            error_message="Username already exists!")

    return render_template('sysuser/useradd.html',form=useradd_form)

##############################################################################################
# USER LIST ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/userlist',methods=['GET','POST'])
@a.admin_required
def userlist():
    '''list out system users'''
    columnHead = ["username","adminpri"]
    userlist = md.System_User.query.all()
    match = []
    for users in userlist:
        temp = [users.username,users.adminpri]
        match.append(temp)
    return render_template('sysuser/userlist.html',PAGE_MAIN_TITLE=const.SERVER_NAME,
        colNum=len(columnHead),matches=match,columnHead=columnHead)

##############################################################################################
# USER MODIFY ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/usermod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def usermod(primaryKey):
    '''modify system user'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.System_User.query.filter(md.System_User.username == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" deleted from the system") #logging
            return redirect(url_for('admintools.userlist',username=current_user.username))

        elif(request.form["button"]=="Modify"):
            adminpri = md.System_User.query.filter(md.System_User.username == primaryKey).first().adminpri
            usermod_form = fm.System_User_EditForm()
            usermod_form.adminPriv.default = ('1' if adminpri else '0')
            usermod_form.process()
            return render_template("sysuser/usermod.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            primaryKey=primaryKey,form = usermod_form)

        elif(request.form["button"]=="Submit Changes"):
            adminpri = request.form.get("adminPriv")
            target_mod = md.System_User.query.filter(md.System_User.username == primaryKey).first()
            target_mod.adminpri = True if adminpri == '1' else False
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('admintools.userlist',username=current_user.username))

        else:
            abort(404)

    else:
        abort(400)

##############################################################################################
# nologin routes (requires no login) PLEASE REFRAIN IN ACTUAL DEPLOYMENT SERVERS
##############################################################################################
@bp.route('/sysuseradd/nologin',methods=['GET','POST'])
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
def useradd_nologin():#This function is for initial server initialization only,
	#NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''Adds a user into system using admintools, no checking is done
    Use only in initial deployment phase, please switch off the routes
    regarding this one it is done. returns 0 on success and 1 on fail'''
    useradd_form = fm.System_User_RegisterForm()
    if useradd_form.validate_on_submit():
        hpass = generate_password_hash(useradd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
        target_add = md.System_User(useradd_form.username.data,hpass,True if int(useradd_form.adminPriv.data) else False)#create user obj
        sq.db_session.add(target_add)#adds user object onto database.
        sq.db_session.commit()
        srvlog["sys"].warning(useradd_form.username.data+ " registered under admintools/nologin ! admin="+str(useradd_form.adminPriv.data)) #logging
        return "admintools : ok" #TODO return a webpage

    return render_template('admintools/sysuseradd.html',form=useradd_form)

##############################################################################################
# Logging routes (display server logs)
# ported from old pyflask project : update2
##############################################################################################
@bp.route('/logs/<logtype>')
@a.admin_required
def logview(logtype):
    #Display logs on the local server
    filebuff = []
    with open( os.path.join(const.LOGS_DIR,logtofile[logtype]) ,'r' ) as f:
        #opens the logfile of required logtype for reading
        for line in f:
            filebuff.append(line)
        if(len(filebuff) == 0):
            filebuff = ["Empty, No logs at the moment"]
        return render_template("admintools/logging.html",
                            	PAGE_MAIN_TITLE=const.SERVER_NAME,
                            	logfile = filebuff)
