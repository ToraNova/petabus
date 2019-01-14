#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Active_Truck(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
        return '<%r %r>' % (self.__tablename__,self.id)

    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Active_Truck"
    # TODO: DEFINE LIST OF COLUMNS
    tracking_number = r.Column(r.String(r.lim.MAX_LOCATION_SIZE), nullable=False, unique=True)
    location1 = r.Column(r.Boolean(),unique=False,nullable=False)
    location2 = r.Column(r.Boolean(),unique=False,nullable=False)
    location3 = r.Column(r.Boolean(),unique=False,nullable=False)
    location4 = r.Column(r.Boolean(),unique=False,nullable=False)
    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Tracking number":"tracking_number",
    "Location 1":"location1",
    "Location 2":"location2",
    "Location 3":"location3",
    "Location 4":"location4",

    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Active_Truck" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {

    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.tracking_number = insert_list["tracking_number"]
        self.location1 = insert_list["location1"]
        self.location2 = insert_list["location2"]
        self.location3 = insert_list["location3"]
        self.location4 = insert_list["location4"]
    ######################################################################################################
