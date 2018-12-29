#--------------------------------------------------
# assert.py
# this file aims to provide wrapper functionality
# for some routes
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm

from functools import wraps

##############################################################################################
# Wrappers
##############################################################################################
def admin_required(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if (not current_user.is_authenticated):
			return render_template("errors/unauthorized.html",
        		displat_message="Login required!")
		elif (not current_user.adminpri):
			return render_template("errors/error.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
				username=current_user.username,
				error_title="Unauthorized",
				error_message="You are not authorized to access this content.")
			#abort(401) #throw unauthorized_request 401
		return fn(*args, **kwargs)
	return decorated_view

def route_disabled(fn):
    #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if (const.DISABLE_CRIT_ROUTE):
			abort(404)
		return fn(*args, **kwargs)
	return decorated_view

def API_checker(fn):
	'''This wrapper checks if the API entered is correct'''
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if ('key' not in request.args):	 # get and check key
			return "Incorrect API call",404
		elif(request.args.get('key')!= const.ADMIN_PLAINT_APIKEY):
			return "Incorrect Key",400
		return fn(*args,**kwargs)
	return decorated_view

def ID_checker(fn):
	@wraps(fn)
	def decorated_view(*args,**kwargs):
		if('f0' not in request.args): 		#f0 stores the ID for the client
			return "f0 unspecified",1 	#this function may be disabled if client uses FIXED IP
		return fn(*args,**kwargs)
	return decorated_view

def Localhost_only(fn):
	@wraps(fn)
	def decorated_view(*args,**kwargs):
		if(request.remote_addr != '127.0.0.1'): #only allows localhost access
			return "localhost access only",1
		return fn(*args,**kwargs)
	return decorated_view
