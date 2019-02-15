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

#namespace class MapBusSocket
#introduced for bustracking on petabus/bustalk 19/02/07
#handles active bus tracking
class MapBusSocket(Namespace):
	target_model = res.active_bus.Active_Bus
	def on_connect(self):
		#sends all active route
		#TODO: sends active routes
		self.sendRouteData()

	def logout_event(self):
		emit('driver_logout',{})

	def on_disconnect(self):
		#do nothing for now upon disconnection
		pass

	def on_routeUpdate(self,json):
		#request info on a particular route
		#TODO responds based on json request
		print("Route Update request on :",json["route_num"])
		self.sendUpdates(json["route_num"])
		pass

	def on_routeData(self):
		#sends new active routes info
		#TODO sends active routes info
		self.sendRouteData()
		pass

	def sendRouteData(self):
		#sends all route data onto client
		#obtains a distinct route list
		distinctRoutelist = self.target_model.query.distinct().group_by(self.target_model.route_num).all()
		rep_json = []
		for d in distinctRoutelist:
			tmp = {}
			tmp["route_num"] = d.route_num
			route_mod = res.georoute.Georoute.query.filter(res.georoute.Georoute.id == d.route_num).first()
			if(route_mod == None):
				tmp["route_name"] = "Not registered"
			else:
				tmp["route_name"] = route_mod.name
			rep_json.append(tmp)
		emit('route_data',{"distinct_routes":rep_json})

	def sendUpdates(self,route_num):
		route_data = self.target_model.query.filter(self.target_model.route_num == route_num).all()
		rep_json = []
		for d in route_data:
			tmp = {}
			tmp["id"] = d.id #the active bus id
			tmp["lati"] = d.long
			tmp["long"] = d.lati
			tmp["busid"] = d.bus_id
			bus_mod = res.bus.Bus.query.filter(res.bus.Bus.reg_no == d.bus_id).first()
			if(bus_mod == None):
				tmp["busreg"] = "Not registered"
			else:
				tmp["busreg"] = bus_mod.reg_no
			rep_json.append(tmp)
		emit('route_update',{"bus_data":rep_json})

#namespace class MapPointSocket
#migrated from socketio.py since u6
#handles display of geopoints on a map.
class MapPointSocket(Namespace):
	target_model = res.geopoint.Geopoint
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
		newmark = self.target_model(insert_list)
		db_session.add(newmark)
		db_session.commit()

	def sendPointData(self):
		#code to send out all geopoints from the db
		pointlist = self.target_model.query.all()
		list = []

		for points in pointlist:
			data_dict = {}
			data_dict["id"] = points.id
			data_dict["long"] = points.long
			data_dict["lati"] = points.lati
			data_dict["time"] = points.time.strftime('%m/%d/%Y %H:%M:%S')
			route = self.target_model.query.filter(
			self.target_model.id == points.route_id ).first()
			if route == None:
				data_dict["route"] = "Unassigned"
			else:
				data_dict["route"] = route.name
			list.append(data_dict)
		#list = str(list)[1:-2]
		#out = json.dumps({"points":list})
		emit('point_data',{"points":list})
