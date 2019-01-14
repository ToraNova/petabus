#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Truck_Log(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Truck_Log"
    # TODO: DEFINE LIST OF COLUMNS
    tracking_number = r.Column(r.String(r.lim.MAX_LOCATION_SIZE), nullable=False, unique=True)
    start_ts = r.Column(r.DateTime, nullable=False)
    end_ts = r.Column(r.DateTime, nullable=False) #latitude
    truck_id = r.Column(r.Integer,nullable=False)
    driver_id = r.Column(r.Integer,nullable=False)
    route_num = r.Column(r.Integer,nullable=False)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Tracking number":"tracking_number",
    "Start Timestamp":"start_ts",
    "End Timestamp":"end_ts",
    "Truck ID":"truck_id",
    "Driver ID":"driver_id",
    "Route Number":"route_num"

    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Truck_Log" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    def __init__(self,insert_list):
        self.tracking_number = insert_list["tracking_number"]
        self.truck_id = insert_list["truck_id"]
        self.driver_id = insert_list["driver_id"]
        self.route_num = insert_list["route_num"]
        self.start_ts = insert_list["start_ts"]
        self.end_ts = insert_list["end_ts"]
    ######################################################################################################
