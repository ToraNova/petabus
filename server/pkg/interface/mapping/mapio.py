#--------------------------------------------------
# mapio.py
# this file contains the socketio class for the
# interface/mapping library
# introduced 3/2/2019
#--------------------------------------------------

#flask socket io
from flask_socketio import Namespace, emit
from pkg.resource import rdef as res #resource importing
from pkg.database.fsqlite import db_session

import datetime

#namespace class MapPointSocket
#migrated from socketio.py since u6
#handles display of geopoints on a map.
class MapPointSocket(Namespace):
	def on_connect(self):
		#upon connection
		self.sendPointData()

	def on_disconnect(self):
		#on disconnect callback
		pass

	def on_update(self):
		#on_update callback
		self.sendPointData()

	def on_pointAdd(self,json):
		self.addPointData(json["lati"],json["long"])

	def addPointData(self,lati,long):
		insert_list = {
		"long":long,
		"lati":lati,
		"time":datetime.datetime.now()
		}
		newmark = res.geopoint.Geopoint(insert_list)
		db_session.add(newmark)
		db_session.commit()

	def sendPointData(self):
		#code to send out all geopoints from the db
		pointlist = res.geopoint.Geopoint.query.all()
		list = []

		for points in pointlist:
			data_dict = {}
			data_dict["id"] = points.id
			data_dict["long"] = points.long
			data_dict["lati"] = points.lati
			data_dict["time"] = points.time.strftime('%m/%d/%Y %H:%M:%S')
			route = res.georoute.Georoute.query.filter(
			res.georoute.Georoute.id == points.route_id ).first()
			if route == None:
				data_dict["route"] = "Unassigned"
			else:
				data_dict["route"] = route.name
			list.append(data_dict)
		#list = str(list)[1:-2]
		#out = json.dumps({"points":list})
		emit('point_data',{"points":list})
