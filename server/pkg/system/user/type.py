#--------------------------------------------------
# type.py
# introduced u4 - 24/01/2019
# used for system user type adding (admin use only)
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

bp = Blueprint('systype', __name__, url_prefix='/sys')

##############################################################################################
# system user type add/mod routes
# USERTYPE ADD
# u4 - introduced usertype, now dynamically generate choices
##############################################################################################
@bp.route('/typeadd',methods=['GET','POST'])
@a.admin_required
def typeadd():
    '''adds a system user type onto the system'''
    typeadd_form = fm.System_UserType_AddForm()
    if typeadd_form.validate_on_submit():
        target_add = md.System_UserType.query.filter(md.System_UserType.typename == typeadd_form.typename.data).first()
        if(target_add == None):
            target_add = md.System_UserType(typeadd_form.typename.data,typeadd_form.prilevel.data)#create usertype obj
            sq.db_session.add(target_add)#adds usertype object onto database.
            sq.db_session.commit()
            srvlog["sys"].info(typeadd_form.typename.data+" registered as new type, prilevel="+typeadd_form.prilevel.data) #logging
            return render_template("standard/message.html",
                display_title="Success",
                display_message="Added "+target_add.typename+" usertype into the system.")

        else:
            return render_template("errors/error.html",
            error_title="Failure",
            error_message="Usertype already exists!")

    return render_template('sysuser/typeadd.html',form=typeadd_form)

##############################################################################################
# USER TYPE LIST ROUTE
# introduced on u4
##############################################################################################
@bp.route('/typelist',methods=['GET','POST'])
@a.admin_required
def typelist():
    '''list out system user types'''
    columnHead = ["usertype","privelege level"]
    userlist = md.System_UserType.query.all()
    match = []
    for type in userlist:
        temp = [type.typename,type.prilevel]
        match.append(temp)
    return render_template('sysuser/typelist.html',
        colNum=len(columnHead),matches=match,columnHead=columnHead)

##############################################################################################
# USER TYPE MODIFY ROUTE
# introduced on u1
##############################################################################################
@bp.route('/typemod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def typemod(primaryKey):
    '''modify system user type'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" usertype deleted from the system") #logging
            return redirect(url_for('systype.typelist'))

        elif(request.form["button"]=="Modify"):
            target_mod = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            usermod_form = fm.System_UserType_EditForm()
            return render_template("sysuser/typemod.html",
            primaryKey=primaryKey,form = usermod_form)

        elif(request.form["button"]=="Submit Changes"):
            target_mod = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            target_mod.usertype = request.form.get("usertype")
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('systype.typelist'))

        else:
            abort(404)
    else:
        abort(400)
