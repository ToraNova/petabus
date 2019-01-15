#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r
import datetime

class Active_Bus(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
        return '<%r %r>' % (self.__tablename__,self.id)

    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Active_Bus"
    # TODO: DEFINE LIST OF COLUMNS
    bus_id = r.Column(r.Integer,nullable=False)
    driver_id = r.Column(r.Integer,nullable=False)
    route_num = r.Column(r.Integer,nullable=False)
    time_stamp = r.Column(r.DateTime,nullable=False)
    long = r.Column(r.Float, nullable=False)
    lati = r.Column(r.Float, nullable=False) #latitude
    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Bus ID":"bus_id",
    "Driver ID":"driver_id",
    "Route":"route_num",
    "Time Stamp":"time_stamp",
    "Longitude":"long",
    "Latitude":"lati"

    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Active_Bus" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {

    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.bus_id = insert_list["bus_id"]
        self.driver_id = insert_list["driver_id"]
        self.route_num = insert_list["route_num"]
        self.time_stamp = insert_list["time_stamp"]
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
    ######################################################################################################
## optional, dateinput time will be adjusted later on
#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
