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
from pkg.resource.busres import bus_driver
from pkg.resource.busres import bus
from pkg.resource.busres import active_bus
from pkg.resource.logres import bus_log
from pkg.resource.logres import loc_log
from pkg.resource.logres import truck_log
from pkg.resource.truckres import truck_driver
from pkg.resource.truckres import truck_system
from pkg.resource.truckres import active_truck
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
    bus_driver.Bus_Driver,
    bus_driver.Bus_Driver_AddForm,
    bus_driver.Bus_Driver_EditForm
    ]
    ,
    "Bus":[
    bus.Bus,
    bus.Bus_AddForm,
    bus.Bus_EditForm
    ]
    ,
    "Active_Bus":[
    active_bus.Active_Bus,
    None,
    None
    ]
    ,
    "Bus_Log":[
    bus_log.Bus_Log,
    None,
    None
    ]
    ,
    "Loc_Log":[
    loc_log.Loc_Log,
    None,
    None
    ]
    ,
    "Truck_Driver":[
    truck_driver.Truck_Driver,
    truck_driver.Truck_Driver_AddForm,
    truck_driver.Truck_Driver_EditForm
    ]
    ,
    "Truck_System":[
    truck_system.Truck_System,
    truck_system.Truck_System_AddForm,
    truck_system.Truck_System_EditForm
    ]
    ,
    "Truck_Log":[
    truck_log.Truck_Log,
    None,
    None
    ]
    ,
    "Active_Truck":[
    active_truck.Active_Truck,
    None,
    None
    ]


}
