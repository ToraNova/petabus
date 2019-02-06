#--------------------------------------------------
# rdef.py
# This file is used to define the resources used in
# the current deployment. It is meant to be dynamic
# refer to readme.txt before editing this file.
# introduced in u3
# ToraNova
#--------------------------------------------------

##########################################################
# PERSISTENT. DO NOT EDIT THIS !
##########################################################
#INDEX LIST enum
sqlClass = 0    #The SQL CLASS object INDEX
aForm = 1       #add form
eForm = 2       #edit form

rgen_keyword = "rgen_" #used to seek out form attributes
rgen_selkey = "rgensel_" #used to seek out SelectField form attr
rgen_timkey = "rgentim_"
rlin_nullk = "-1"
##########################################################

#IMPORT RESOURCE CLASS HERE (MODEL AND FORMS)
from pkg.resource.geores import geopoint
from pkg.resource.geores import georoute

from pkg.resource.generic import param3model

##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
##########################################################

dist_resources = {
    "Georoute":[
    georoute.Georoute,
    georoute.AddForm,
    georoute.EditForm
    ]
    ,
    "Geopoint":[
    geopoint.Geopoint,
    geopoint.AddForm,
    geopoint.EditForm
    ]
    ,
    "Param3":[
    param3model.Param3,
    None,
    None
    ]
}
