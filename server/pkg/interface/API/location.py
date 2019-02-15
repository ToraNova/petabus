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

import pkg.const as const
from pkg.database import models as md
from pkg.system import assertw as a

from pkg.resource.logres import bus_loc_log as loclog
from pkg.resource.logres import bus_log as buslog

from pkg.database import fsqlite as sq
from pkg.resource.busres import bus #SAMPLE ONLY, DO NOT USE FOR ACTUAL DEPLOYMENT
from pkg.resource.busres import active_bus
from sqlalchemy import func

from pkg.interface.mapping.mapio import MapBusSocket

import datetime
#primary blueprint
bp = Blueprint('busLocAPI', __name__, url_prefix='/push')
##############################################################################################
# API push routings
##############################################################################################

@bp.route('/bus/location/begin')
def busLocAPI():

    upload_ip = request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    upload_argTotal = 5

        #check for missing argument
    for idx in range(upload_argTotal):
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))

    upload_bufferArr=[]

    for idx in range(upload_argTotal):
        upload_bufferArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY

    print() #DEBUGGING ONLY


    start_time = datetime.datetime.now()
    target_list = active_bus.Active_Bus.query.filter(active_bus.Active_Bus.bus_id == upload_bufferArr[0], active_bus.Active_Bus.driver_id == upload_bufferArr[1], active_bus.Active_Bus.route_num == upload_bufferArr[2]).first()

    if (target_list == None):

        insert_list = { "bus_id":upload_bufferArr[0],"driver_id":upload_bufferArr[1],"route_num":upload_bufferArr[2],"time_stamp":start_time,"long":upload_bufferArr[3], "lati":upload_bufferArr[4], "current_seqno": 1}
        target_add = active_bus.Active_Bus(insert_list)
        try:
            sq.db_session.add(target_add)
            sq.db_session.commit()

            ab_busid = active_bus.Active_Bus.query.filter(active_bus.Active_Bus.driver_id == upload_bufferArr[1]).first()
            curtime =datetime.datetime.now()
            insert_list= { "activebus_id":ab_busid.id,"time_stamp":curtime,"long":upload_bufferArr[3], "lati":upload_bufferArr[4]}
            buslocationlog =  loclog.Bus_Loc_Log(insert_list)
            print(ab_busid.id)

            try:
                sq.db_session.add(buslocationlog)
                sq.db_session.commit()
                return 'add successfully'

            except Exception as e:
                print(str(e))
                sq.db_session.rollback()
                return 'add - couldnt add log'


        except Exception as e:
            print(str(e))
            sq.db_session.rollback()

            curtime =datetime.datetime.now()
            insert_list = {"activebus_id":999,"time_stamp":curtime,"long": 999, "lati": 999}
            buslocationlog =  loclog.Bus_Loc_Log(insert_list)

            try:
                sq.db_session.add(buslocationlog)
                sq.db_session.commit()
                return 'failtoadd'

            except Exception as e:
                sq.db_session.rollback()
                return 'failtoadd - couldnt add log'

    else:
        target_mod = active_bus.Active_Bus.query.filter(active_bus.Active_Bus.driver_id == upload_bufferArr[1]).first()

        if target_mod == None:
            return '1'

        target_mod.driver_id = upload_bufferArr[1]
        target_mod.long = upload_bufferArr[3]
        target_mod.lati = upload_bufferArr[4]
        target_mod.current_seqno = target_mod.current_seqno + 1

        ab_busid = active_bus.Active_Bus.query.filter(active_bus.Active_Bus.driver_id == upload_bufferArr[1]).first()

        try:
            sq.db_session.add(target_mod)
            sq.db_session.commit()

            curtime = datetime.datetime.now()
            insert_list = { "activebus_id":ab_busid.id,"time_stamp":curtime,"long":upload_bufferArr[3], "lati":upload_bufferArr[4]}
            buslocationlog =  loclog.Bus_Loc_Log(insert_list)
            if (target_mod.current_seqno == 5):
                target_mod.current_seqno = 0
                try:
                    sq.db_session.add(buslocationlog)
                    sq.db_session.commit()
                    return 'update log successfully'
                except Exception as e:
                    sq.db_session.rollback()
                    return 'update - couldnt add log'
            else:
                return 'updated database'

        except Exception as e:
            sq.db_session.rollback()

            curtime = datetime.datetime.now()
            insert_list = { "activebus_id":999,"time_stamp":curtime,"long": 999, "lati": 999}
            buslocationlog =  loclog.Bus_Loc_Log(insert_list)
            try:
                sq.db_session.add(buslocationlog)
                sq.db_session.commit()
                return 'failtoupdate'
            except Exception as e:
                sq.db_session.rollback()
                return 'failtoupdate - couldnt add log'

@bp.route('/bus/location/logout')
def buslogoutAPI():

        upload_ip = request.remote_addr
        print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
        upload_argTotal = 1 #driverid only
            #check for missing argument
        for idx in range(upload_argTotal):
            if( 'f'+str(idx) not in request.args):
                return ("Missing argument "+'f'+str(idx))

        #upload_buffer[0] = driver_id
        upload_targetArr=[]
        for idx in range(upload_argTotal):
            upload_targetArr.append(request.args.get('f'+str(idx)))
            print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY

        #print() #DEBUGGING ONLY
        target_del = active_bus.Active_Bus.query.filter(upload_targetArr[0] == active_bus.Active_Bus.driver_id).first()
        timestop = datetime.datetime.now()

        insert_list = {"start_ts":target_del.time_stamp,"end_ts":timestop, "bus_id":target_del.bus_id,"driver_id":target_del.driver_id,"activebus_id":target_del.id,"route_num":target_del.route_num}
        target_add = buslog.Bus_Log(insert_list)
        try:
            sq.db_session.add(target_add)
            sq.db_session.delete(target_del)
            sq.db_session.commit()
            return '0'
        except Exception as e:
            sq.db_session.rollback()
            return '1'





#################################################################################################################################################################################################################################3
#end
########################################################################################################################################################################################################################################
        #if busdetails == None:
         #  return '1'

        #busdetails.start_ts = target_del.time_stamp
        #busdetails.end_ts = timestop
        #busdetails.bus_id = target_del.bus_id
        #busdetails.driver_id = target_del.driver_id
        #busdetails.route_num = target_del.route_num

        #try:
        #    sq.db_session.add(busdetails)
        #    sq.db_session.commit()
        #    sq.db_session.delete(target_del)
        #    sq.db_session.commit()
        #    return '0'

        #except Exception as e:
        #    sq.db_session.rollback()
        #    return '1'


        #insert_log = { "start_ts": databuslog[0], "end_ts": databuslog[1], "bus_id": databuslog[2], "driver_id": databuslog[3], "activebus_id": databuslog[4], "route_num":databuslog[5]}
        #busdetails = buslog.Bus_Log(insert_log)
    #    try:
            #sq.db_session.add(busdetails)
            #sq.db_session.commit()

        #    sq.db_session.delete(target_del)
        #    sq.db_session.commit()
        #    return "logout"

    #    except Exception as e:
    #        sq.db_session.rollback()
    #        return "fail to add to bus log / delete table"

############################################################################################################################
##@bp.route('/bus/location/add')
##def busLocAPI_add(): #fixed on 19/1/16 by ToraNova


##    upload_ip=request.remote_addr
##    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
##    upload_argTotal = 6

        #check for missing argument
##    for idx in range(upload_argTotal):
##        if( 'f'+str(idx) not in request.args):
##            return ("Missing argument "+'f'+str(idx))
#    for row in range(upload_argTotal):
#        data={\
#            "busid"=row[0],
#            "driverid"=row[1],
#            "routenum"=row[2],
#            "longitude"=row[3],
#            "latitude"=row[4]
#        }
#    if((data)not in request.args):
#        for
#        return ("Missing argument "+'f'+str(idx))

##    upload_locationArr = []
    #Argument Obtain, get all arguments and store in an array
##    for idx in range(upload_argTotal):
##        upload_locationArr.append(request.args.get('f'+str(idx)))
##        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY


    #obtain uploader's IP address
##    print() #DEBUGGING ONLY

    #bus_regno = bus.Bus.query.filter( bus.Bus.reg_no == upload_locationArr[0]).first()
    #upload_locationArr[0]
    #if (bus_regno):

    #busid = bus.Bus.query.filter()
##    timenow = time.strftime('%A %B, %d %Y %H:%M:%S')
##   insert_list1 = { "reg_no":upload_locationArr[0],"driver_id":upload_locationArr[1],"route_num":upload_locationArr[2],"time_stamp":timenow}
##    insert_list2 = { "id":upload_locationArr[0],"long":upload_locationArr[3],"lati":upload_locationArr[4],"reg_no":upload_locationArr[5]}
##    target_add1 = active_bus.Active_Bus(insert_list1)
##    target_add2 = bus.Bus(insert_list2)

##    try:
##        sq.db_session.add(target_add1)
##        sq.db_session.add(target_add2)
##        sq.db_session.commit()
##        srvlog["oper"].info("push/bus/location ADD :"+str(upload_locationArr))
##        return '0'
##    except Exception as e:
##        sq.db_session.rollback()
###        srvlog["oper"].error("push/bus/location FAIL :"+str(upload_locationArr))
##        return '1'
    #else:
    #    return "Invalid Bus"

##@bp.route('/bus/location/update')
##def busLocAPI_upd(): #fixed on 19/1/16 by ToraNova

##    upload_ip=request.remote_addr
##    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
##    upload_argTotal = 6
##    for idx in range(upload_argTotal):
        #check for missing argument
##        if( 'f'+str(idx) not in request.args):
##            return ("Missing argument "+'f'+str(idx))

##    upload_locationArr = []
    #Argument Obtain, get all arguments and store in an array
##    for idx in range(upload_argTotal):
##        upload_locationArr.append(request.args.get('f'+str(idx)))
##        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY
    #obtain uploader's IP address
##    print() #DEBUGGING ONLY

##    target_mod1 = active_bus.Active_Bus.query.filter(
##        getattr(active_bus.Active_Bus,active_bus.Active_Bus.bus_id) == upload_locationArr[0]  ).first()
##    target_mod1.driver_id = upload_locationArr[1]
##    target_mod1.route_num = upload_locationArr[2]
##    target_mod2 = bus.Bus.query.filter(
##        getattr(bus.Bus,bus.Bus.rlist_priKey) == upload_locationArr[0] ).first()
##    target_mod2.long = upload_locationArr[3]
##    target_mod2.lati = upload_locationArr[4]
##    target_mod2.reg_no = upload_locationArr[5]
##    if target_mod1 and target_mod2 == None:
##            return '1'

##    try:
##        sq.db_session.add(target_mod1)
##        sq.db_session.add(target_mod2)
##        sq.db_session.commit()
##        srvlog["oper"].info("push/bus/location MOD :"+str(upload_locationArr))
##        return '0'
##    except Exception as e:
##        sq.db_session.rollback()
##        srvlog["oper"].error("push/bus/location FAIL :"+str(upload_locationArr))
##        return '1'
