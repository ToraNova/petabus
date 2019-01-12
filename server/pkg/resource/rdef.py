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
##########################################################

#IMPORT RESOURCE CLASS HERE (MODEL AND FORMS)
from pkg.resource.geores import geopoint
from pkg.resource.geores import georoute
from pkg.resource.geores import geopath
from pkg.resource.busres import driver
from pkg.resource.busres import bus_system
from pkg.resource.busres import active_bus

##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
##########################################################

dist_resources = {
    "Georoute":[
    georoute.Georoute,
    georoute.Georoute_AddForm,
    georoute.Georoute_EditForm
    ]
    ,
    "Geopoint":[
    geopoint.Geopoint,
    geopoint.Geopoint_AddForm,
    geopoint.Geopoint_EditForm
    ]
    ,
    "Geopath":[
    geopath.Geopath,
    geopath.Geopath_AddForm,
    None
    ]
    ,
    "Bus_Driver":[
    driver.Bus_Driver,
    driver.Bus_Driver_AddForm,
    driver.Bus_Driver_EditForm
    ]
    ,
    "Bus_System":[
    bus_system.Bus_System,
    bus_system.Bus_System_AddForm,
    bus_system.Bus_System_EditForm
    ]
    ,
    "Active_Bus":[
    active_bus.Active_Bus,
    active_bus.Active_Bus_AddForm,
    None 
    ]


}
