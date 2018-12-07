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

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a
import pkg.fsqlite as sq #extra for any db commits

bp = Blueprint('admintools', __name__, url_prefix='/admintools')

##############################################################################################
# TableList routes / Admin Tools
##############################################################################################
@bp.route('/sysuseradd',methods=['GET','POST'])
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
def admintools_useradd():#This function is for initial server initialization only,
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
        # logger["user"].info(
        # 		in_form.username.data+
        # 		" registered as new user under admintools, admin="+
        #  		str(in_form.adminPriv.data)
        # 		) #TODO logging
        return "admintools : ok" #TODO return a webpage

    return render_template('admintools/sysuseradd.html',form=useradd_form)
