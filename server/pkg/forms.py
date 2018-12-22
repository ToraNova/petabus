#--------------------------------------------------
# forms.py
# this file holds the form definitions
# they are used in conjunction with the templates
# created 8/12/2018
#--------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SelectField, IntegerField, RadioField
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length, NumberRange

import pkg.limits as lim # limits import

##############################################################################################
# Essential Forms (similar for each pyFlask deployment) Edited as of R7
##############################################################################################

class LoginForm(FlaskForm): #Last Edit R7
	#define a flask form "LoginForm" with 3 fields
	#a string field named username,with validators
	username = StringField('username',
		validators=[InputRequired(),Length(min=lim.MIN_USERNAME_SIZE,max=lim.MAX_USERNAME_SIZE)])
	password = PasswordField('password',
		validators=[InputRequired(),Length(min=lim.MIN_PASSWORD_SIZE,max=lim.MAX_PASSWORD_SIZE)])
	#rememberMe = BooleanField('remember me')

class System_User_RegisterForm(FlaskForm): #Last Edit R7
	username = StringField('username',
		validators=[InputRequired(),Length(min=lim.MIN_USERNAME_SIZE,max=lim.MAX_USERNAME_SIZE)])
	password = PasswordField('password',
		validators=[InputRequired(),Length(min=lim.MIN_PASSWORD_SIZE,max=lim.MAX_PASSWORD_SIZE)])
	adminPriv = SelectField('administrator privelege ?',choices=[('0','No admin privelege'),('1','Grant admin privelege')])
	#adminPrive = BooleanField("administrator ?")

class System_User_EditForm(FlaskForm): #Last Edit R8
	adminPriv = SelectField('administrator privelege ?',choices=[('0','No admin privelege'),('1','Grant admin privelege')])

##############################################################################################
# Admin Forms - Edits
##############################################################################################
class Configuration_EditForm(FlaskForm):
	config_value = StringField('Config Value',
		validators=[InputRequired(),Length(min=2,max=lim.MAX_CONFIG_VALU_SIZE)])
	fieldlist = ['config_value']

##############################################################################################
# Distribution dependent forms
##############################################################################################

##############################################################################################
# From YT - correction needed
##############################################################################################

class Data_ViewForm(Flask Form):
	bustype = StringField('bus_type', validators=[InputRequired(),Length(min=2,max=10)])
	buslist = SelectField('bus_schedule',choices=[('0','Non Working Bus'),('1','Working Bus')])
