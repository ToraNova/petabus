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
from pkg.system import assertw as a
from pkg.resource.busres import active_bus
from datetime import datetime
from pkg.database.fsqlite import db_session
from pkg.database import fsqlite as sq

#primary blueprint
bp = Blueprint('maptrack2', __name__, url_prefix='/track')

@bp.route('/basic1')
def basic():
	columnHead = ["Route Number"]
	#date = datetime(2012,3,3,10,10,10)
	#insert_list = {"bus_id":8,"driver_id":8,"route_num":1,"time_stamp":date,"long":2.925297,"lati":101.642064,"current_seqno":1}
	#target_add = active_bus.Active_Bus(insert_list)
	#sq.db_session.add(target_add)
	#sq.db_session.commit()

	routelist = active_bus.Active_Bus.query.all()
	route = []
	for basic in routelist:
		tempo = [basic.route_num]
		if(tempo in route):
			pass
		else:
			route.append(tempo)
			print(route)
	#return render_template('flask_io/basic_map.html')

	return render_template('flask_io/meimap.html',MAPWIDTH=1500,MAPHEIGHT=900,routenum = route, length=len(route),columnHead=columnHead)

@bp.route('/geolocation')
def point():
	#return render_template('flask_io/basic_map.html')
    return render_template('flask_io/pointloc.html',MAPWIDTH=800,MAPHEIGHT=800)
