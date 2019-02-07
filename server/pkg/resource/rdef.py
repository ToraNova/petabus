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

from pkg.resource.busres import bus_driver
from pkg.resource.busres import bus
from pkg.resource.busres import active_bus
from pkg.resource.logres import bus_log
from pkg.resource.logres import bus_loc_log
from pkg.resource.logres import truck_loc_log
from pkg.resource.logres import truck_log
from pkg.resource.truckres import truck_driver
from pkg.resource.truckres import truck
from pkg.resource.truckres import active_truck

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
    None
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
    "Bus_Loc_Log":[
    bus_loc_log.Bus_Loc_Log,
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
    "Truck":[
    truck.Truck,
    truck.Truck_AddForm,
    truck.Truck_EditForm
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
    ,
    "Truck_Loc_Log":[
    truck_loc_log.Truck_Loc_Log,
    None,
    None
    ]
}
