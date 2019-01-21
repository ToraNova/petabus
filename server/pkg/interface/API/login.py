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
from pkg.resource.busres import bus
from pkg.resource.geores import georoute
from pkg.resource.r import getMatch

from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

import time
#primary blueprint
bp = Blueprint('driverloginAPI', __name__, url_prefix='/push')

##############################################################################################
# API push routings
#############################################################################################
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

    target_driver= bus_driver.Bus_Driver.query.filter(upload_driverArr[0] == bus_driver.Bus_Driver.id).first()
    if target_driver == None:
        return '1'
    else:
        if target_driver.password == upload_driverArr[1]:
            response = required_Response("Bus","Georoute")
            return response
        else:
            return '1'

def column(matrix, i):
   return [row[i] for row in matrix]

def required_Response(tablename1,tablename2):
    #upload_ip=request.remote_addr
    #print("Pull request from host ",upload_ip,tablename1,tablename2,'list') #DEBUGGING ONLY
    out=''
    try:
        match1 = getMatch(tablename1)[1]
        # #------------FORMATTING
        s1 = column(match1, 1)
        out += "bus_no="
        if s1 != None:
            for row in s1:
                #for field in row:
                    out += str(row)
                    if row != s1[-1]:
                        out += ','
                    else:
                        out += ';'
        # #//----------FORMATTING
        match2 = getMatch(tablename2)[1]
        # #------------FORMATTING
        s2 = column(match2, 0)
        out += "route_no="
        if s1 != None:
            for row in s2:
                #for field in row:
                    out += str(row)
                    if row != s2[-1]:
                        out += ','
                    else:
                        out += ';'
        # #//----------FORMATTING
        return out
    except Exception as e:
        return '1'
