#--------------------------------------------------
# res_import.py
# This file serves to reduce the code size of each res
# one can simply import this file and it imports the
# required modules for res model and form defines
# introduced in u3
# ToraNova
#--------------------------------------------------

#SAMPLE USAGE
# type the following in your resource file
# from pkg.resource import res_import as r
# then to use Column, it is just r.Column

###############################################################################
# STANDARD MODEL USAGE IMPORTS (COPY PASTA THIS!)-----------------------------
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from pkg.database.fsqlite import Base    #fsqlite dependency
from pkg import limits as lim     #lim dependency
import datetime
#-----------------and the forms--this as well!--------------------------------
from flask_admin.form.widgets import DatePickerWidget
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SelectField, IntegerField, RadioField
from wtforms import SubmitField, SelectMultipleField, DateField
from wtforms.validators import InputRequired, Email, Length, NumberRange
###############################################################################

from pkg.resource.rdef import rlin_nullk

#useful function for checking on null selections
def checkNull(list,colName):
    if(list.get(colName) == rlin_nullk):
        return None
    else:
        return list.get(colName)
