#--------------------------------------------------
# mapping.py
# an initial test for mapping on flask servers
# this now contains some example for geopoints u6
# introduced 8/1/2019
# last update 3/2/2019
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
from pkg.resource import rdef as res

#primary blueprint
bp = Blueprint('maptrack', __name__, url_prefix='/track')

@bp.route('/basic')
def basic():
	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/basic.html')

@bp.route('/geopoint')
@login_required
def point():
	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/dashboard.html')
