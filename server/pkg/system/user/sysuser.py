#--------------------------------------------------
# sysuser.py
# introduced u4 - 24/01/2019
# used for system user adding (admin)
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user

import pkg.const as const
from pkg.database import models as md
from pkg.database import fsqlite as sq #extra for any db commits
from pkg.database import forms as fm
from pkg.system import assertw as a
from pkg.system.auth import removeTokenFile
from pkg.system.servlog import srvlog,logtofile

bp = Blueprint('sysuser', __name__, url_prefix='/sys')

##############################################################################################
# system user add/mod routes
# USER ADD ROUTE
# introduced update1
# last edit : update4
# u4 - introduced usertype, now dynamically generate choices
# removed system username on route url.
##############################################################################################
@bp.route('/useradd',methods=['GET','POST'])
@a.admin_required
def useradd():
    '''adds a system user onto the system'''
    useradd_form = fm.System_User_RegisterForm()
    useradd_form.usertype.choices = tupleGenerator(md.System_UserType.query.all())
    if useradd_form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.username == useradd_form.username.data).first()
        if(target_user == None):
            hpass = generate_password_hash(useradd_form.password.data,method=const.HASH_ALGORITHM_0)#password hashing
            target_add = md.System_User(useradd_form.username.data,hpass,useradd_form.usertype.data)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            srvlog["sys"].info(useradd_form.username.data+" registered as new user, type="+useradd_form.usertype.data) #logging
            return render_template("standard/message.html",
                display_title="Success",
                display_message="Added "+target_add.username+" into the system.")

        else:
            return render_template("errors/error.html",
            error_title="Failure",
            error_message="Username already exists!")

    return render_template('sysuser/useradd.html',form=useradd_form)

##############################################################################################
# USER LIST ROUTE
# introduced update1
# last edit : update4
# removed system username on route url.
##############################################################################################
@bp.route('/userlist',methods=['GET','POST'])
@a.admin_required
def userlist():
    '''list out system users'''
    columnHead = ["username","usertype","privilege level"]
    userlist = md.System_User.query.all()
    match = []
    for users in userlist:
        temp = [users.username,users.getUserType(),users.getPriLevel()]
        match.append(temp)
    return render_template('sysuser/userlist.html',
        colNum=len(columnHead),matches=match,columnHead=columnHead)

##############################################################################################
# USER MODIFY ROUTE
# introduced update1
# last edit : update4
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
            return redirect(url_for('sysuser.userlist'))

        elif(request.form["button"]=="Modify"):
            target_mod = md.System_User.query.filter(md.System_User.username == primaryKey).first()
            usermod_form = fm.System_User_EditForm()
            usermod_form.usertype.choices = tupleGenerator(md.System_UserType.query.all())
            usermod_form.usertype.default = target_mod.usertype
            usermod_form.process()
            return render_template("sysuser/usermod.html",
            primaryKey=primaryKey,form = usermod_form)

        elif(request.form["button"]=="Submit Changes"):
            target_mod = md.System_User.query.filter(md.System_User.username == primaryKey).first()
            target_mod.usertype = request.form.get("usertype")
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('sysuser.userlist'))

        elif(request.form["button"]=="Change Password"):
            userid = md.System_User.query.filter(md.System_User.username == primaryKey).first().id
            return redirect(url_for('auth.tokengen',issue="pwreset", param=userid))

        else:
            abort(404)
    else:
        abort(400)

##############################################################################################
# Auxiliary functions
# updated from r.py on u4.
##############################################################################################

def tupleGenerator(sqlresult): #FOR USERTYPE SQLRESULTS ONLY !
	'''takes in the sql result, parses the output to allow generation of
	a dynamic WTF select field this takes in a list of 3-tuples, merges
	the last two into a string and spits a list of 2-tuples used together with
	getattr(form,sfield).choices = dynamicSelectorHandler(query_all result,which element)'''
	outList = []
	for elements in sqlresult:
		outList.append((elements.id,elements.typename))

	return outList
