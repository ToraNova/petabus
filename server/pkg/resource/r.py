#--------------------------------------------------
# r.py <DONOT USE! WIP>!!
# this file contains functions and routes
# for admin usage
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
from pkg.database import models as md
from pkg.database import fsqlite as sq #extra for any db commits
from pkg.interface import forms as fm
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile

#additional overheads
import os

bp = Blueprint('resource', __name__, url_prefix='/resource')

##############################################################################################
# Resource-table # RESOURCES ARE ACTORS/ENTITIES IN THE SYSTEM. TRUCKS, STUDENTS ... etc
# ported from oldpyflask 29/12/2018
##############################################################################################
@routed_app.route('/radd/<tablename>', methods=['GET','POST'])
@admin_required
# The route for resource adding (check fform and fdist)
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def radd(tablename):
	resadd_form = dist.dist_resources[tablename][dist.fdist_global_RForm]()
	if resadd_form.validate_on_submit():
		return dist.radd_handler(resadd_form,tablename,flog_main,froute_global_debug)
	return render_template('res/radd0.html',PAGE_MAIN_TITLE=server_title,
	form = resadd_form, tablename=tablename)

@routed_app.route('/rlist/<tablename>',methods=['GET','POST'])
@login_required
# The route for resource listing
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rlist(tablename):
	columnHead = dist.getMatch(tablename)[0]
	match = dist.getMatch(tablename)[1]
	display_tablename = dist.dist_resources[tablename][dist.fdist_global_sqlClass].rlist_dis
	return render_template('res/datalist0.html',PAGE_MAIN_TITLE=server_title,
	colNum=len(columnHead),matches=match,columnHead=columnHead, tablename=tablename,
	data_table_name=display_tablename)

@routed_app.route('/rmod/<tablename>/<primaryKey>',methods=['GET','POST'])
@admin_required
# The route for resource modification.
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rmod(tablename,primaryKey):
	if(request.method=="POST"):
		if(request.form["button"]=="Delete"):
			dist.rdel_handler(tablename,primaryKey,flog_main,froute_global_debug)
			return redirect(url_for('resource.rlist',username=current_user.username,tablename=tablename))
		elif(request.form["button"]=="Modify"):
			return dist.rpremod_handler(tablename,primaryKey,froute_global_debug)
		elif(request.form["button"]=="Submit Changes"):
			dist.rposmod_handler(request.form,tablename,primaryKey,flog_main,froute_global_debug)
			return redirect(url_for('resource.rlist',username=current_user.username,tablename=tablename))
		else:
			abort(404)
	else:
		abort(400)
