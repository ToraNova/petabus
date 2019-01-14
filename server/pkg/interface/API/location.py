#--------------------------------------------------
# location.py
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
from pkg.resource.busres import bus #SAMPLE ONLY, DO NOT USE FOR ACTUAL DEPLOYMENT
from pkg.resource.busres import active_bus
import time
#primary blueprint
bp = Blueprint('push', __name__, url_prefix='/push')

##############################################################################################
# API push routings
##############################################################################################
@bp.route('/bus/location/add')
def addGP3():

    upload_ip=request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
    upload_argTotal = 6

        #check for missing argument
    for idx in range(upload_argTotal):
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))
#    for row in range(upload_argTotal):
#        data={
#            "busid"=row[0],
#            "driverid"=row[1],
#            "routenum"=row[2],
#            "longitude"=row[3],
#            "latitude"=row[4]
#        }
#    if((data)not in request.args):
#        for
#        return ("Missing argument "+'f'+str(idx))

    upload_locationArr = []
    #Argument Obtain, get all arguments and store in an array
    for idx in range(upload_argTotal):
        upload_locationArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY


    #obtain uploader's IP address
    print() #DEBUGGING ONLY
    timenow = time.strftime('%A %B, %d %Y %H:%M:%S')
    insert_list1 = { "bus_id":upload_locationArr[0],"driver_id":upload_locationArr[1],"route_num":upload_locationArr[2],"time_stamp":timenow}
    insert_list2 = { "id":upload_locationArr[0],"long":upload_locationArr[3],"lati":upload_locationArr[4],"reg_no":upload_locationArr[5]}
    target_add1 = active_bus.Active_Bus(insert_list1)
    target_add2 = bus.Bus(insert_list2)

    try:
        sq.db_session.add(target_add1)
        sq.db_session.add(target_add2)
        sq.db_session.commit()
        srvlog["oper"].info("push/bus/location ADD :"+str(upload_locationArr))
        return '0'
    except Exception as e:
        sq.db_session.rollback()
        srvlog["oper"].error("push/bus/location FAIL :"+str(upload_locationArr))
        return '1'

@bp.route('/bus/location/update')
def updateGP3():

    upload_ip=request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
    upload_argTotal = 6
    for idx in range(upload_argTotal):
        #check for missing argument
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))

    upload_locationArr = []
    #Argument Obtain, get all arguments and store in an array
    for idx in range(upload_argTotal):
        upload_locationArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY
    #obtain uploader's IP address
    print() #DEBUGGING ONLY

    target_mod1 = active_bus.Active_Bus.query.filter(
        getattr(active_bus.Active_Bus,active_bus.Active_Bus.bus_id) == upload_locationArr[0]  ).first()
    target_mod1.driver_id = upload_locationArr[1]
    target_mod1.route_num = upload_locationArr[2]
    target_mod2 = bus.Bus.query.filter(
        getattr(bus.Bus,bus.Bus.rlist_priKey) == upload_locationArr[0] ).first()
    target_mod2.long = upload_locationArr[3]
    target_mod2.lati = upload_locationArr[4]
    target_mod2.reg_no = upload_locationArr[5]
    if target_mod1 and target_mod2 == None:
            return '1'

    try:
        sq.db_session.add(target_mod1)
        sq.db_session.add(target_mod2)
        sq.db_session.commit()
        srvlog["oper"].info("push/bus/location MOD :"+str(upload_locationArr))
        return '0'
    except Exception as e:
        sq.db_session.rollback()
        srvlog["oper"].error("push/bus/location FAIL :"+str(upload_locationArr))
        return '1'
