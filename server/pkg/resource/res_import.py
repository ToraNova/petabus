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
#-----------------and the forms--this as well!--------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField
from wtforms import SelectField, IntegerField, RadioField
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length, NumberRange,DataRequired
###############################################################################
