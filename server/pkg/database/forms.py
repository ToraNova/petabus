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
# u4 - added System_UserType forms
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
	usertype = SelectField('usertype',choices=[])

class System_User_URLRegisterForm(FlaskForm): #Last Edit R7
	username = StringField('username',
		validators=[InputRequired(),Length(min=lim.MIN_USERNAME_SIZE,max=lim.MAX_USERNAME_SIZE)])
	password = PasswordField('password',
		validators=[InputRequired(),Length(min=lim.MIN_PASSWORD_SIZE,max=lim.MAX_PASSWORD_SIZE)])

class System_User_URLPasswordResetForm(FlaskForm): #Last Edit R7
	password = PasswordField('new password',
		validators=[InputRequired(),Length(min=lim.MIN_PASSWORD_SIZE,max=lim.MAX_PASSWORD_SIZE)])

class System_User_EditForm(FlaskForm): #Last Edit R8
	usertype = SelectField('usertype',choices=[])

################################################################################################

prilevels = [
    ('0','0:Administrator (Highest Privilege)'),
	('1','1:Can view/add all resources/operation without restrictions'),
	('2','2:Can view all resources/operation'),
	('3','3:Can view some resources/operation'),
	('4','4:Unimplemented'),
	('5','5:Unimplemented'),
	('6','6:Unimplemented'),
	('7','7:Unimplemented'),
	('8','8:Unimplemented'),
	('9','9:Guest Accounts/Visitors (Lowest Privilege)')
		]

class System_UserType_AddForm(FlaskForm): #u4 introduction
	#to allow admins to add new user types
	typename = StringField('typename (no capitals)',
		validators=[InputRequired(),Length(min=lim.MIN_USERNAME_SIZE,max=lim.MAX_USERNAME_SIZE)])
	prilevel = SelectField('privilege level (0:highest, 9:lowest)',
		choices=prilevels)

class System_UserType_EditForm(FlaskForm):
	prilevel = SelectField('privilege level (0:highest, 9:lowest)',
		choices=prilevels)

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
