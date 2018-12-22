from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.models as md
import pkg.forms as fm
import pkg.assertw as a
import pkg.fsqlite as sq #extra for any db commits

bp = Blueprint('dataview', __name__, url_prefix='/dataview')

@bp.route('/bus_view',methods=['GET','POST'])

def buslist():
    '''list out system bus'''
    busview_form = fm.Data_ViewForm()
