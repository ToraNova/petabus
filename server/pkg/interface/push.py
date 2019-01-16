#--------------------------------------------------
# push.py
# this file is for API routings, particularly pushing data
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
from pkg.database import models as md
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile
from pkg.database import fsqlite as sq
from pkg.resource.generic import param3model #SAMPLE ONLY, DO NOT USE FOR ACTUAL DEPLOYMENT

#primary blueprint
bp = Blueprint('push', __name__, url_prefix='/push')

##############################################################################################
# API push routings
##############################################################################################
@bp.route('/generic/param3/add')
#This route allows API callers to add an entry
def addGP3():

    upload_ip=request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
    upload_argTotal = 3
    for idx in range(upload_argTotal):
        #check for missing argument
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))

    upload_bufferArr = []
    #Argument Obtain, get all arguments and store in an array
    for idx in range(upload_argTotal):
        upload_bufferArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY
    #obtain uploader's IP address
    print() #DEBUGGING ONLY

    insert_list = { "param0":upload_bufferArr[0],"param1":upload_bufferArr[1],"param2":upload_bufferArr[2]}
    target_add = param3model.Param3(insert_list)

    try:
        sq.db_session.add(target_add)
        sq.db_session.commit()
        srvlog["oper"].info("push/generic/param3 ADD :"+str(upload_bufferArr))
        return '0'
    except Exception as e:
        sq.db_session.rollback()
        srvlog["oper"].error("push/generic/param3 FAIL :"+str(upload_bufferArr))
        return '1'

@bp.route('/generic/param3/update')
#This route allows API users to update an entry
def updateGP3():

    upload_ip=request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
    upload_argTotal = 4
    for idx in range(upload_argTotal):
        #check for missing argument
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))

    upload_bufferArr = []
    #Argument Obtain, get all arguments and store in an array
    for idx in range(upload_argTotal):
        upload_bufferArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY
    #obtain uploader's IP address
    print() #DEBUGGING ONLY

    target_mod = param3model.Param3.query.filter(
        getattr(param3model.Param3,param3model.Param3.rlist_priKey) == upload_bufferArr[0] ).first()
    if target_mod == None:
        return '1'
    target_mod.param0 = upload_bufferArr[1]
    target_mod.param1 = upload_bufferArr[2]
    target_mod.param2 = upload_bufferArr[3]

    try:
        sq.db_session.add(target_mod)
        sq.db_session.commit()
        srvlog["oper"].info("push/generic/param3 MOD :"+str(upload_bufferArr))
        return '0'
    except Exception as e:
        sq.db_session.rollback()
        srvlog["oper"].error("push/generic/param3 FAIL :"+str(upload_bufferArr))
        return '1'
