#--------------------------------------------------
# Source.py
# this file sources the main flask object
# it also generates the the object
# based on configuration files
# created 8/12/2018
# author : ToraNova
#--------------------------------------------------

from flask import Flask
from flask import Blueprint
import pkg.const as const
from flask_login import LoginManager
from flask import render_template

from pkg.database.fsqlite import db_session
from flask_socketio import SocketIO

def server(config=None):
	#create and configures the server
	out = Flask(__name__, instance_relative_config=True)
	out.config.from_mapping(
		SECRET_KEY='mmubus',
		DATABASE=const.DB00_NAME
		#check out out.instance_path
	)

	if config is None:
		out.config.from_pyfile('config.py',silent=True)
	else:
		out.config.from_mapping(config)

	from pkg.interface import socketio #socket io import
	from pkg.interface.mapping import mapio

	from pkg.interface import home
	from pkg.interface.mapping import debugging,tracking
	from pkg.interface.API import push,pull
	from pkg.system import auth,admintools
	from pkg.system.user import sysuser,type,sysnologin
	from pkg.resource import r

	#######################################################################################################
	# Login manager section
	#######################################################################################################
	login_manager = LoginManager()
	login_manager.init_app(out)
	@out.login_manager.user_loader
	def load_user(id): #loads a sql object model as "login-ed"
		target_user = auth.sysuser_getobj(id)
		return target_user

	@out.login_manager.unauthorized_handler
	def unauthorized_warning():
		return render_template("errors/unauthorized.html",
			displat_message="Login required!")
	login_manager.login_view = "login"
	login_manager.login_message = "Please login first."
	login_manager.login_message_category = "info"

	bplist = [	r.bp,auth.bp,home.bp,admintools.bp,socketio.bp,
				push.bp,pull.bp,sysuser.bp,type.bp,sysnologin.bp,
				debugging.bp,tracking.bp]

	for bp in bplist:
		out.register_blueprint(bp)

	#tear down context is done here.
	@out.teardown_appcontext
	def shutdown_session(exception=None):
		db_session.remove()


	# FLASK SOCKET USE 8/1/2019
	out_nonsock = out
	out = SocketIO(out_nonsock)
	out.on_namespace(socketio.SystemUtilNamespace('/sysutil'))
	out.on_namespace(mapio.MapPointSocket('/geopoint'))

	return out,out_nonsock
