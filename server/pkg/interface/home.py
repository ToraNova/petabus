#--------------------------------------------------
# home.py
# this file serves home/dashboard routes
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
from pkg.database import models as md
from pkg.interface import forms as fm
from pkg.system import assertw as a

#primary blueprint
bp = Blueprint('home', __name__, url_prefix='')

##############################################################################################
# Index routings
##############################################################################################
@bp.route('/')
def index():
	return redirect(url_for("auth.login"))

@bp.route('/<username>/home',methods=['GET','POST'])
@login_required
def home(username):
	return render_template("standard/welcome.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
	username=current_user.username)

####################################################################################
# favicon
####################################################################################
@bp.route('/favicon.ico')
def favicon():
	return redirect(url_for('static',filename='favicon.ico'))
