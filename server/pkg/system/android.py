#this file is for the route between server and android



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
from pkg.database.fsqlite import init_db

bp = Blueprint('android', __name__, url_prefix='/location')
