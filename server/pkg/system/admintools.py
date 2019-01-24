#--------------------------------------------------
# admintools.py
# this file contains functions and routes
# for admin usage
# introduced 8/12/2018
# removed the useradd route from this file, migrated to sysuser under user (u4)
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
from pkg.database import models as md
from pkg.database import fsqlite as sq #extra for any db commits
from pkg.database import forms as fm
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile

from pkg.system.user.sysuser import tupleGenerator

#additional overheads
import os
from pkg.database.fsqlite import init_db

bp = Blueprint('admintools', __name__, url_prefix='/admintools')

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
    useradd_form.usertype.choices = tupleGenerator(md.System_UserType.query.all())
    if useradd_form.validate_on_submit():
        hpass = generate_password_hash(useradd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
        try:
            target_add = md.System_User(useradd_form.username.data,hpass,useradd_form.usertype.data)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            srvlog["sys"].warning(useradd_form.username.data+ " registered under admintools/nologin ! type="+useradd_form.usertype.data) #logging
            return "admintools : ok" #TODO return a webpage
        except Exception as e:
            sq.db_session.rollback() #rollback errors
            print("[ER]",__name__," Exception has occurred:",str(e))
            srvlog["sys"].warning("Sysuseradd/nologin with exception "+str(e)) #logging
            return "admintools : failed"

    return render_template('admintools/sysuseradd.html',form=useradd_form)

@bp.route('/resetdb')
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
def resetdb():
    #NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''resets the database with the default user admin
    this way, the metadata and schema is also recreated.
    DO NOT USE DURING DEPLOYMENT'''
    try:
        if(os.path.isfile('temp.db')):
            os.remove('temp.db')
        if(os.path.isfile(os.path.join(const.TOKN_DIR,"init.token"))):
            os.remove(os.path.join(const.TOKN_DIR,"init.token"))
        init_db()
        print("[IF]",__name__," Database reset.")
        srvlog["sys"].warning("Database reset under admintools/resetdb") #logging
        return "admintools : ok"
    except Exception as e:
        print("[ER]",__name__," Exception has occurred:",str(e))
        srvlog["sys"].warning("Database reset with exception "+str(e)) #logging
        return "admintools : fail"

##############################################################################################
# Logging routes (display server logs)
# ported from old pyflask project : update4
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
        return render_template("admintools/logging.html",logfile = filebuff)
