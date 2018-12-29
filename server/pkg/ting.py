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
            target_add = md.Bus_Driver(busadd_form.busname.data,busadd_form.busroute.data,True if int(busadd_form.busStatus.data) else False)#create user obj
            sq.db_session.add(target_add)#adds user object onto database.
            sq.db_session.commit()
            #srvlog["sys"].info(busadd_form.busname.data+" registered as new user) #logging
            return render_template("message.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
                busname=current_user.username,
                display_title="Success",
                display_message="Added "+target_add.busname+" into the system.")

    return render_template('yt-busadd.html',form=busadd_form)

@bp.route('/bus_view',methods=['GET','POST'])
def buslist():
#    '''list out system bus'''
#    busview_form = fm.Data_ViewForm()
#    return render_template('/buslist.html',form=busview_form)
    '''list out bus users'''
    columnHead = ["busname","busroute","bus status"]
    buslist = md.Bus_Driver.query.all()
    match = []
    for users in buslist:
        temp = [users.busname,users.busroute,users.busStatus]
        match.append(temp)
    return render_template('yt-buslist.html',PAGE_MAIN_TITLE=const.SERVER_NAME,
        colNum=len(columnHead),matches=match,columnHead=columnHead)


@bp.route('/busmod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def busmod(primaryKey):
    '''modify bus user'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.Bus_Driver.query.filter(md.Bus_Driver.busname == primaryKey).first()
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            srvlog["sys"].info(primaryKey+" deleted from the system") #logging
            return redirect(url_for('dataview.buslist'))

        elif(request.form["button"]=="Modify"):
            target_busroute = md.Bus_Driver.query.filter(md.Bus_Driver.busname == primaryKey).first().busroute
            busmod_form = fm.Bus_Driver_EditForm()
            target_busroute = busmod_form.busroute
            busmod_form.process()
            target_busstatus = md.Bus_Driver.query.filter(md.Bus_Driver.busname == primaryKey).first().busStatus
            busmod_form.status.default = ('1' if target_busstatus else '0')
            busmod_form.process()
            return render_template("yt-busmod.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
            primaryKey=primaryKey,form = busmod_form)
###need correction :D
        elif(request.form["button"]=="Submit Changes"):
            #target_busroute = request.form.get("busroute")
            target_mod = md.Bus_Driver.query.filter(md.Bus_Driver.busname == primaryKey).first()
            #target_mod.busroute = target_busroute
            busStatus = request.form.get("status")
            target_mod.busstatus = True if busStatus == '1' else False
            sq.db_session.add(target_mod)
            sq.db_session.commit()
            return redirect(url_for('dataview.buslist',username=current_user.username))
