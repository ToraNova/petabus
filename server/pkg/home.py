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
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a

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
	return render_template("welcome.html",PAGE_MAIN_TITLE=const.SERVER_NAME,
	username=current_user.username)

####################################################################################
# favicon
####################################################################################
@bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('static',filename='favicon.ico'))
