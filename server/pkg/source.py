#--------------------------------------------------
# Source.py
# this file sources the main flask object
# it also generates the the object
# based on configuration files
# created 8/12/2018
#--------------------------------------------------

from flask import Flask
from flask import Blueprint
import pkg.const as const
from pkg.fsqlite import db_session
from flask_login import LoginManager

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

	from pkg import auth,home,admintools,dataview


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

	out.register_blueprint(auth.bp)
	out.register_blueprint(home.bp)
	out.register_blueprint(admintools.bp)
	out.register_blueprint(dataview.bp)

	#tear down context is done here.
	@out.teardown_appcontext
	def shutdown_session(exception=None):
		db_session.remove()

	return out
