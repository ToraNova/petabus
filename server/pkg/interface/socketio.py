#--------------------------------------------------
# socketio.py
# basic file that handles socket io use-cases
# introduced 8/1/2019
#--------------------------------------------------

from flask import Blueprint
from flask_socketio import Namespace, emit
from flask import render_template, redirect, url_for
import datetime

import pkg.const as const
import pkg.resource.rdef as res
from pkg.resource.busres import active_bus
from pkg.resource.busres import bus
import json

bp = Blueprint('sock', __name__, url_prefix='') #flask sock bp

#----------------------------------------------------------------------------------------
# ROUTES
#----------------------------------------------------------------------------------------

@bp.route('/sampleflask',methods=['GET','POST'])
def sample():
	return render_template('flask_io/sample.html',PAGE_MAIN_TITLE=const.SERVER_NAME)

@bp.route('/sysclock',methods=['GET','POST'])
def sysclock():
	return render_template('flask_io/sysclock.html',PAGE_MAIN_TITLE=const.SERVER_NAME)

#----------------------------------------------------------------------------------------
# callbacks
#----------------------------------------------------------------------------------------
class StandardIfaceNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_handle_message(self,message):
        print('received message: '+ message)

    def on_handle_json(self,json):
        print('received json: '+ str(json))

    def on_handle_custom_event(self,json):
        print('custom event: '+str(json))

#SystemUtilNamespace is a socket.io class that handles system utility realtime
#data, currently implemented methods is the on_sync_time that allows a realtime
#clock on the server - 8/1/2019 ToraNova
#TODO: implement mapping system
class SystemUtilNamespace(Namespace):
	def on_connect(self):
		print("sysutil on_connect")

	def on_disconnect(self):
		print("sysutil on_disconnect")

	def on_sync_time(self,json):
		#print("callback:",json['data'])
		dTString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		emit('recv_sync', {"datetime":dTString})

class MapDisplayNamespace(Namespace):
	def on_connect(self):
		#self.sendPointData2()
		pass

	def on_disconnect(self):
		pass

	def on_update(self):
		self.sendPointData2()

	def sendPointData(self):
		pointlist = res.geopoint.Geopoint.query.all()
		list = []
		for points in pointlist:
			data_dict = {}
			data_dict["id"] = points.id
			data_dict["long"] = points.long
			data_dict["lati"] = points.lati
			route = res.georoute.Georoute.query.filter(
				res.georoute.Georoute.id == points.route_id ).first()
			data_dict["route"] = route.name
			list.append(data_dict)
		#list = str(list)[1:-2]
		#out = json.dumps({"points":list})
		emit('point_data',{"points":list})

	def sendPointData2(self):
		pointlist = active_bus.Active_Bus.query.all()
		#pointbus = bus.Bus.query.filter(bus.Bus.id == pointlist.bus_id).first()
		list = []
		for points in pointlist:
			data_dict = {}
			data_dict["bus_id"] = points.bus_id
			data_dict["driver_id"] = points.driver_id
			data_dict["long"] = points.long
			data_dict["lati"] = points.lati
			#route = active_bus.Active_Bus.query.filter(
			#	active_bus.Active_Bus.route_num == points.route_num ).first()
			data_dict["route_num"] = points.route_num
			busregno = bus.Bus.query.filter(bus.Bus.id == points.bus_id).first().reg_no #1 object
			data_dict["reg_no"] = busregno
			#route.route
			list.append(data_dict)
			#list2.append(pointbus)
		#list2 = []
		#pointbus = bus.Bus.query.filter(bus.Bus.id == list).first()
		#for ptbus in pointbus:
		#	data2_dict = {}
		#	data2_dict["id"] = ptbus.id
		#	data2_dict["reg_no"] = points.reg_no

		#	list2.append(data2_dict)
		#list = str(list)[1:-2]
		#out = json.dumps({"points":list})
		emit('point_data2',{"points":list})
