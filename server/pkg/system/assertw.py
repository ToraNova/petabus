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
from pkg.database import models as md
from pkg.database import fsqlite as sq #extra for any db commits
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile

from functools import wraps
import os

##############################################################################################
# Wrappers
##############################################################################################
def admin_required(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if (not current_user.is_authenticated):
			return logandDisplay("Unauthenticated access","Unauthenticated. Please login first !")
		elif ( current_user.getPriLevel() != 0 ):
			return render_template("errors/error.html",
				username=current_user.username,
				error_title="Unauthorized",
				error_message="You are not authorized to access this content.")
			#abort(401) #throw unauthorized_request 401'
		else:
			#here if user is admin and already logged in
			return fn(*args, **kwargs)
	return decorated_view

def token_check(fn):
	'''this wrapper checks if the token exist, deletes it if it does and allow
	entry to the route, else, it denies entry and logs the incident'''
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if ( "token" not in request.args):
			return logandDisplay("Invalid token attempt","Unauthorized, please contact administrator.")
		else:
			#check if token is valid
			if(os.path.isfile(os.path.join(const.TOKN_DIR,const.TOKN_SYS,request.args.get("token")))):
				#token exists
				return fn(*args, **kwargs) #allow access
			else:
				return logandDisplay("Invalid token attempt","Unauthorized, please contact administrator.")

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

def logandDisplay(logtitle,display_msg):
	'''using errors/unauthorized, logs and display the error msg'''
	srvlog["sys"].warning(logtitle+" from "+request.remote_addr) #logging
	return render_template("errors/unauthorized.html",
		display_message=display_msg)
