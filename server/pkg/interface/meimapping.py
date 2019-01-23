#--------------------------------------------------
# mapping.py
# an initial test for mapping on flask servers
# introduced 8/1/2019
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
from pkg.interface import forms as fm
from pkg.system import assertw as a

#primary blueprint
bp = Blueprint('maptrack2', __name__, url_prefix='/track')

@bp.route('/basic1')
def basic():
	#return render_template('flask_io/basic_map.html')
	return render_template('flask_io/meimap.html',MAPWIDTH=500,MAPHEIGHT=500)

@bp.route('/geolocation')
def point():
	#return render_template('flask_io/basic_map.html')
    return render_template('flask_io/pointloc.html',MAPWIDTH=800,MAPHEIGHT=800)
