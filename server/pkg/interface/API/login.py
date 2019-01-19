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
from pkg.resource.busres import bus_driver
import time
#primary blueprint
bp = Blueprint('driverloginAPI', __name__, url_prefix='/push')

##############################################################################################
# API push routings
##############################################################################################
@bp.route('/driver/login/valid')
def driverloginAPI_add(): #fixed on 19/1/16 by ToraNova

    upload_ip=request.remote_addr
    print("Uploaded from host ",upload_ip,end=': ') #DEBUGGING ONLY
    #Argument Parsing, requires 20 arguments f0,f1 ... f19 (quarryTrack)
    #Attemoni - 5 arguments
    upload_argTotal = 2

        #check for missing argument
    for idx in range(upload_argTotal):
        if( 'f'+str(idx) not in request.args):
            return ("Missing argument "+'f'+str(idx))

    upload_driverArr = []
    #Argument Obtain, get all arguments and store in an array
    for idx in range(upload_argTotal):
        upload_driverArr.append(request.args.get('f'+str(idx)))
        print('f'+str(idx)+"="+request.args.get('f'+str(idx)),end=' ') #DEBUGGING ONLY

    #print() #DEBUGGING ONLY
    #insert_list = { "id":upload_driverArr[0],"password":upload_driverArr[1] }
    #target_add = bus_driver.Bus_Driver(insert_list)

    #if(upload_driverArr):
    target_driver= bus_driver.Bus_Driver.query.filter(upload_driverArr[0] == bus_driver.Bus_Driver.id).first()
    if(target_driver):
        target_pw = bus_driver.Bus_Driver.query.filter(bus_driver.Bus_Driver.password == upload_driverArr[1]).first()
        if (target_pw):
            return "Correct password!"  # need to redirect url?
        else:
            return "Wrong password!"
    else:
        return "Invalid driver id"
