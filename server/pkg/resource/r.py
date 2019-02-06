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
from flask_login import current_user,login_required

import pkg.const as const
from pkg.database import fsqlite as sq #extra for any db commits
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile
#from pkg.database import models as md #!!MODELS FROM DATABASE ARE NOT USED IN r.PY
#from pkg.interface import forms as fm #!!FORMS FROM INTERFACE ARE NOT USED IN r.PY

#r.py (u3) uses the dist dictionary from rdef
from pkg.resource import rdef
from pkg.resource.res_import import checkNull

#additional overheads
import os
import datetime

bp = Blueprint('resource', __name__, url_prefix='/resource')

##############################################################################################
# Resource-table # RESOURCES ARE ACTORS/ENTITIES IN THE SYSTEM. TRUCKS, STUDENTS ... etc
# ported from oldpyflask 29/12/2018
##############################################################################################

@bp.route('/radd/<tablename>', methods=['GET','POST'])
@a.admin_required
# The route for resource adding (check fform and fdist)
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def radd(tablename):

	resadd_form = rdef.dist_resources[tablename][rdef.aForm]() #creates an ADD FORM

	resadd_form = regenerateForm(resadd_form,None)
	#resadd_form.process()

	if resadd_form.validate_on_submit():
		d_point = getFormAttrList(resadd_form) #d_point has a dictionary for obj creation
		res_model = rdef.dist_resources[tablename][rdef.sqlClass]
		try:
			#try to add
			target_add = res_model(d_point)
			sq.db_session.add(target_add)
			sq.db_session.commit()
			return render_template("standard/message.html",
                display_title="Success",
                display_message="Added resource to system.")
		except Exception as e:
			print(str(e))
			sq.db_session.rollback() #immediately rollback changes
			return render_template("errors/error.html",
            error_title="Failure",
            error_message=str(e))

	return render_template('res/radd0.html',
	form = resadd_form, tablename=tablename)

@bp.route('/rlist/<tablename>',methods=['GET','POST'])
@login_required
# The route for resource listing
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rlist(tablename):
	columnHead = getMatch(tablename)[0]
	match = getMatch(tablename)[1]
	display_tablename = rdef.dist_resources[tablename][rdef.sqlClass].rlist_dis
	return render_template('res/datalist0.html',
	colNum=len(columnHead),matches=match,columnHead=columnHead, tablename=tablename,
	data_table_name=display_tablename)

@bp.route('/rmod/<tablename>/<primaryKey>',methods=['GET','POST'])
@a.admin_required
# The route for resource modification.
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rmod(tablename,primaryKey):
	if(request.method=="POST"):
		res_model = rdef.dist_resources[tablename][rdef.sqlClass]
		if(request.form["button"]=="Delete"):
			#DELETION PROCEDURE
			target_del =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey ).first()
			sq.db_session.delete(target_del)
			sq.db_session.commit()
			return redirect(url_for('resource.rlist',tablename=tablename))

		elif(request.form["button"]=="Modify"):

			if(rdef.dist_resources[tablename][rdef.eForm] == None):
				#edits disabled
				return render_template("errors/error.html",
	            error_title="Modify Failure",
	            error_message="This resource cannot be modified!")

			rmod_form = rdef.dist_resources[tablename][rdef.eForm]() #generates the edit form
			target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey).first()
			#target_mod is the resource entity that we wish to edit
			rmod_form = regenerateForm(rmod_form,target_mod)

			# for a in dir(rmod_form): #for all form attributes
			# 	if a.startswith(rdef.rgen_keyword): #only the ones defined under rgen
			# 		model_field = a[len(rdef.rgen_keyword):]
			# 		rmod_form.__getattribute__(a).default = target_mod.__getattribute__(model_field)
			# 	elif a.startswith(rdef.rgen_selkey):
			# 		model_field = a[len(rdef.rgen_selkey):]
			# 		fkeyres = rdef.dist_resources[rmod_form.fkeyList[model_field][0]][rdef.sqlClass].query.all()
			# 		rmod_form.__getattribute__(a).choices = dynamicSelectorHandler(fkeyres,rmod_form.fkeyList[model_field][1])

			rmod_form.process()
			return render_template('res/rmod0.html',
			primaryKey=primaryKey,tablename=tablename,form=rmod_form)

		elif(request.form["button"]=="Submit Changes"):
			target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey).first()
			for f,name in request.form.items():
				if f.startswith(rdef.rgen_keyword): #only the ones defined under rgen
					model_field = f[len(rdef.rgen_keyword):]
					target_mod.__setattr__(model_field,request.form.get(f))
				elif f.startswith(rdef.rgen_timkey):
					#time processing
					model_field = f[len(rdef.rgen_timkey):]
					target_mod.__setattr__(model_field,
						datetime.datetime.strptime(request.form.get(f), "%Y-%m-%d"))
				elif f.startswith(rdef.rgen_selkey):
					model_field = f[len(rdef.rgen_selkey):]
					target_mod.__setattr__(model_field,checkNull(request.form,f))

			sq.db_session.add(target_mod)
			sq.db_session.commit()
			return redirect(url_for('resource.rlist',tablename=tablename))
		else:
			abort(404)
	else:
		abort(400)

##############################################################################################
# Auxiliary methods, these methods aid the generelization of resource models/forms
##############################################################################################
def getMatch(tablename):
	'''obtains matching columns and data of a specific table
	updated on u3 compared to r9. now supports a cleaner model side requirement'''
	entityClass = rdef.dist_resources[tablename][rdef.sqlClass]
	reslist = entityClass.rlist # the rlist element
	rawlist = entityClass.query.all() # all the records
	columnHead = []
	match = []
	for key,val in reslist.items():
		columnHead.append(key) #adds keys in rlist dictionary to columnHeads

	for entry in rawlist:
		temp = []
		for key in reslist:
			if(reslist[key].startswith("__link__")):
				try:
					rkey = reslist[key].split('/')[1]
					refTable = entityClass.rlink[rkey][0]
					refFKey = entityClass.rlink[rkey][1]
					refLook = entityClass.rlink[rkey][2]
					refEntClass = rdef.dist_resources[refTable][rdef.sqlClass]
					if(entry.__getattribute__(rkey) == None):
						aptTar = "Unlinked"
					else:
						aptTar = refEntClass.query.filter(
							getattr(refEntClass,refFKey) ==
							entry.__getattribute__(rkey)
						).first().__getattribute__(refLook)
				except Exception as e:
					#revert to simple display of id
					#error must have occured here
					# TODO: Logging
					print(str(e))
					aptTar = entry.__getattribute__(rkey)
				finally:
					temp.append(aptTar)
			else:
				temp.append(entry.__getattribute__(reslist[key]))
			print(temp[-1])
		match.append(temp)
	return [columnHead,match]

def getAttrList(in_obj):
	'''returns a list of attributes of an object, not including
	methods and intrinsic attribute another model of this is under
	auxtools in libraries/python/pymod'''
	out = []
	for a in dir(in_obj):
		if not a.startswith('__') and not callable(getattr(in_obj,a)):
			out.append(a)
	return out

def getFormAttrList(form_obj):
	'''returns the data of a form. the keyword is rgen_
	it returns a dictionary with the attribute name striped of rgen_
	as the key and value of the actual data'''
	out = {}
	for a in dir(form_obj):
		if a.startswith(rdef.rgen_keyword):
			out[a[len(rdef.rgen_keyword):]]=form_obj.__getattribute__(a).data
		elif a.startswith(rdef.rgen_selkey):
			out[a[len(rdef.rgen_selkey):]]=form_obj.__getattribute__(a).data
	return out

def regenerateForm(in_form,target=None):
	for a in dir(in_form): #for all form attributes
		if a.startswith(rdef.rgen_keyword) and target != None: #only the ones defined under rgen
			model_field = a[len(rdef.rgen_keyword):] #FOR MODIFY ONLY
			in_form.__getattribute__(a).default = target.__getattribute__(model_field)
		elif a.startswith(rdef.rgen_selkey):
			model_field = a[len(rdef.rgen_selkey):]
			fkeyres = rdef.dist_resources[in_form.fKeylist[model_field][0]][rdef.sqlClass].query.all()
			in_form.__getattribute__(a).choices = dynamicSelectorHandler(fkeyres,in_form.fKeylist[model_field][1])
			if(target != None):
				in_form.__getattribute__(a).default = target.__getattribute__(model_field)
	return in_form


def dynamicSelectorHandler(sqlresult,ref_elem):
	'''takes in the sql result, parses the output to allow generation of
	a dynamic WTF select field this takes in a list of 3-tuples, merges
	the last two into a string and spits a list of 2-tuples used together with
	getattr(form,sfield).choices = dynamicSelectorHandler(query_all result,which element)'''
	outList = []
	for elements in sqlresult:
		outList.append((str(elements.__getattribute__(elements.rlist_priKey)),elements.__getattribute__(ref_elem)))

	outList.append((rdef.rlin_nullk,'No Link'))

	return outList
