from pkg.resource import res_import as r

class Bus_Loc_Log(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Bus_Loc_Log"
    # TODO: DEFINE LIST OF COLUMNS
    activebus_id = r.Column(r.Integer,nullable=False)
    long = r.Column(r.Float, nullable=False)
    lati = r.Column(r.Float, nullable=False) #latitude
    time_stamp = r.Column(r.DateTime, nullable=False)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Log Number":"id",
    "Active Bus id":"activebus_id",
    "Longitude":"long",
    "Latitude":"lati",
    "Time stamp":"time_stamp"

    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Bus_Loc_Log" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    def __init__(self,insert_list):
        self.activebus_id = insert_list["activebus_id"]
        self.time_stamp = insert_list["time_stamp"]
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
    ######################################################################################################
