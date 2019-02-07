#--------------------------------------------------
# debugging.py
# this module serves solely to debug the mapping interface
# for now it is still not portable for other usages
# introduced 3/2/2019
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

#flask socket io
from flask_socketio import Namespace, emit

import pkg.const as const
from pkg.database import models as md
from pkg.system import assertw as a
from pkg.resource import rdef as res

#primary blueprint
bp = Blueprint('mapdebug', __name__, url_prefix='/tools')

@bp.route('/pin_geopoint')
@login_required
def pinpoint():
	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/tooladd.html')
