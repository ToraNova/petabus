#--------------------------------------------------
# auth.py
# this file is meant to store routes for authentication
# purposes such as login/logout or any other administr
# tasks
# introduced 8/12/2018
#--------------------------------------------------

#security and login imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a
from pkg.servlog import srvlog

#primary blueprint
bp = Blueprint('auth', __name__, url_prefix='')

#######################################################################################################
# Routing section
#######################################################################################################
@bp.route('/login', methods=['GET','POST'])
def login():
    userlogin_form = fm.LoginForm()
    if userlogin_form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.username == userlogin_form.username.data).first()
        if(target_user == None):
            #user does inexistent
            return render_template("errors/invalid_login.html",
            display_message="User does not exist!")
        else:
            if(check_password_hash(target_user.password,userlogin_form.password.data)):
                #successful login
                srvlog["user"].info(userlogin_form.username.data+" logged onto the system") #logging
                login_user(target_user)#login_manager logins
                return redirect(url_for("home.home",username=target_user.username))
            else:
                #incorrect password
                return render_template("errors/invalid_login.html",
                display_message="Invalid password")
    return render_template('login.html',form=userlogin_form)

@bp.route('/<username>/logout')
@login_required
def logout(username):
    logout_username = current_user.username
    logout_user()
    srvlog["user"].info(logout_username+" logged out the system") #logging
    return redirect(url_for("auth.login"))

def sysuser_getobj(id):
	return md.System_User.query.filter(md.System_User.id == id).first()
