from pkg.resource import res_import as r

class Truck_Loc_Log(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Truck_Loc_Log"
    # TODO: DEFINE LIST OF COLUMNS
    loc = r.Column(r.String(r.lim.MAX_LOCATION_SIZE), nullable=False, unique=False)
    time_stamp = r.Column(r.DateTime, nullable=False)
    tracking_num = r.Column(r.String(r.lim.MAX_LOCATION_SIZE), nullable=False, unique=False)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Log Number":"id",
    "Location":"loc",
    "Time stamp":"time_stamp",
    "Tracking Number":"tracking_num",
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Truck_Loc_Log" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    def __init__(self,insert_list):
        self.id = insert_list["id"]
        self.loc = insert_list["loc"]
        self.time_stamp = insert_list["time_stamp"]
        self.tracking_num = insert_list["tracking_num"]
    ######################################################################################################
