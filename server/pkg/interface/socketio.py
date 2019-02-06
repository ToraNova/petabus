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
import json

bp = Blueprint('sock', __name__, url_prefix='') #flask sock bp

#----------------------------------------------------------------------------------------
# ROUTES
#----------------------------------------------------------------------------------------

@bp.route('/sampleflask',methods=['GET','POST'])
def sample():
	return render_template('flask_io/sample.html')

@bp.route('/sysclock',methods=['GET','POST'])
def sysclock():
	return render_template('flask_io/sysclock.html')

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
