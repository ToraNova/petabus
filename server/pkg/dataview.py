#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, NumberRange

import pkg.limits as lim # limits import

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

bp = Blueprint('mei', __name__, url_prefix='/databus')

##############################################################################################
# system user add/mod routes
# USER ADD ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/bus_Add',methods=['GET','POST'])
@a.admin_required
def bus_Add():
    '''adds a system user onto the system'''
    bus_Add_form = fm.Data_Bus_RegisterForm()
    if bus_Add_form.validate_on_submit():
        target_user = md.Data_Bus.query.filter(md.Data_Bus.busname == bus_Add_form.busname.data).first()
        if(target_user == None):
            target_add = md.Data_Bus(bus_Add_form.busname.data,bus_Add_form.busdriver.data,True if int(bus_Add_form.busstatus.data) else False)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            srvlog["sys"].info(bus_Add_form.busname.data+" registered as new bus, busdriver="+bus_Add_form.busdriver.data+"bus status as "+str(bus_Add_form.busstatus.data)) #logging
            return render_template("message.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            display_title="Success", display_message="Added "+target_add.busname+ "driver = "+ target_add.busdriver+" into the system.")

        else:
            return render_template("error.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            #busname=current_user.username,
            error_title="Failure",
            error_message="Username already exists!")

    return render_template('busadd.html',form=bus_Add_form)

##############################################################################################
# USER LIST ROUTE
# last edit : update2
# removed system username on route url.
##############################################################################################
@bp.route('/buslist',methods=['GET','POST'])
@a.admin_required
def buslist():
    '''list out system users'''
    columnHead = ["bus_id","busname","busdriver","bus_status"]
    buslist = md.Data_Bus.query.all()
    match = []
    for users in buslist:
        temp = [users.id,users.busname,users.busdriver,users.busstatus]
        match.append(temp)
    return render_template('buslist.html',PAGE_MAIN_TITLE=const.SERVER_NAME,
        colNum=len(columnHead),matches=match,columnHead=columnHead)

@bp.route('/bus_Add',methods=['GET','POST'])
##############################################################################################
# USER MODIFY ROUTE
# last edit : update2
# removed system username on ro-ute url.
##############################################################################################
@bp.route('/busmod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def busmod(primaryKey):
    '''modify system user'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.Data_Bus.query.filter(md.Data_Bus.id == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" deleted from the system") #logging
            return redirect(url_for('mei.buslist'))

        elif(request.form["button"]=="Modify"):
            busdriver = md.Data_Bus.query.filter(md.Data_Bus.id == primaryKey).first().busdriver
            busstatus = md.Data_Bus.query.filter(md.Data_Bus.id == primaryKey).first().busstatus
            busmod_form = fm.Data_Bus_EditForm()
            busmod_form.busdriver = StringField('busdriver',
        	validators=[InputRequired(),Length(min=lim.MIN_USERNAME_SIZE,max=lim.MAX_USERNAME_SIZE)])
            busmod_form.busstatus.default = ('1' if busstatus else '0')
            busmod_form.process()
            return render_template("busmod.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            primaryKey=primaryKey,form = busmod_form)

        elif(request.form["button"]=="Submit Changes"):
            busdriver = request.form.get("busdriver")
            busstatus = request.form.get("busstatus")
            target_mod = md.Data_Bus.query.filter(md.Data_Bus.id == primaryKey).first()
            target_mod.busdriver= busdriver
            target_mod.busstatus = True if busstatus == '1' else False
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('mei.buslist'))

        else:
            abort(404)

    else:
        abort(400)
