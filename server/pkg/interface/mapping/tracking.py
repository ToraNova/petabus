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

from pkg.resource.busres import active_bus as actbus
from pkg.resource.geores import geopoint as geo
from time import gmtime, strftime
from pkg.database import fsqlite as sq
from datetime import datetime

from pkg.resource import rdef as res


#primary blueprint
bp = Blueprint('maptrack', __name__, url_prefix='/track')

@bp.route('/basic')
def basic():
	#return render_template('flask_io/basic_map.html')

	columnHead = ["Route Number"]
	routelist = actbus.Active_Bus.query.all()
	Route = []
	for basic in routelist:
		tempo = [basic.route_num]
		Route.append(tempo)

	return render_template('flask_io/basic_map_test.html',MAPWIDTH=500,MAPHEIGHT=500,routenum = Route,colNum=len(columnHead),columnHead=columnHead)

	#return render_template('leaflet/geopoint/basic.html')


@bp.route('/geopoint')
@login_required
def point():

	#PLEASE DO NOT WORK ON EXAMPLE SECTIONS !!!
	#PLEASE !

	# n=0
	# columnHead = ["Latitude","Longitude"]
	#point = Route 1
	#insert_list = { "bus_id":1134,"driver_id":43657,"route_num":1,"time_stamp":timenow,"long"=upload_bufferArr[3], "lati" = upload_bufferArr[4]}
    #target_add = active_bus.Active_Bus(insert_list)
	#sq.db_session.add(target_add)
    #sq.db_session.commit()
	#nowtime = datetime.datetime.now()
	# date = datetime(2012, 3, 3, 10, 10, 10)
	# insert_list = { "bus_id":8,"driver_id":8,"route_num":1,"time_stamp":date,"long":2.925297, "lati" :101.642064,"current_seqno":1}
	# target_add = actbus.Active_Bus(insert_list)
	# sq.db_session.add(target_add)
	# sq.db_session.commit()
	# pointlist = actbus.Active_Bus.query.all()
	# latlong = []
	# for point in pointlist:
	# 	temp = [point[n].lati,point[n].long]
	# 	latlong.append(temp)
	# 	n=n+1
	# return render_template('flask_io/pointdisp.html',MAPWIDTH=800,MAPHEIGHT=800,latlong= latlong,num = n,colNum=len(columnHead),columnHead=columnHead)

	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/dashboard.html')

#Route for active_bus tracking on end-user UI side
#ToraNova 2019/02/07
@bp.route('/active_bus')
def active_bus():
	return render_template('leaflet/active_bus/jackboard.html')
	#return render_template('leaflet/active_bus/dashboard.html')
