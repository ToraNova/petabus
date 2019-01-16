#--------------------------------------------------
# pull.py
# pull is to query server using an URL API.
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
from pkg.resource.r import getMatch

#primary blueprint
bp = Blueprint('busId_API', __name__, url_prefix='/pull')

##############################################################################################
# API pull routings
##############################################################################################
@bp.route('/bus_info/<tablename1>/<tablename2>/list')
#This route allows API callers to add an entry
def tableList(tablename1,tablename2):

    upload_ip=request.remote_addr
    print("Pull request from host ",upload_ip,tablename1,tablename2,'list') #DEBUGGING ONLY

    try:
        match1 = getMatch(tablename1)[1]
        # #------------FORMATTING
        out = ''
        def column(matrix, i):
           return [row[i] for row in matrix]
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
        srvlog["oper"].error("busId_API/{}/list FAIL :".format(tablename1))
        return '1'
