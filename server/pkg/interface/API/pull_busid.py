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
from pkg.resource.generic import param3model #SAMPLE ONLY, DO NOT USE FOR ACTUAL DEPLOYMENT
from pkg.resource.r import getMatch

#primary blueprint
bp = Blueprint('pull', __name__, url_prefix='/pull')

##############################################################################################
# API pull routings
##############################################################################################
@bp.route('/<tablename>/list')
#This route allows API callers to add an entry
def tableList(tablename):

    upload_ip=request.remote_addr
    print("Pull request from host ",upload_ip,tablename,'list') #DEBUGGING ONLY

    try:
        match = getMatch(tablename)[1]
        # #------------FORMATTING
        # out = ''
        # for row in match:
        #     for field in row:
        #         out += str(field)
        #         if( )
        #     out += ';'
        # #//----------FORMATTING
        out = str(match)
        return out
    except Exception as e:
        srvlog["oper"].error("pull/{}/list FAIL :".format(tablename))
        return '1'
