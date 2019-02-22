#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Sensors(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "Sensors"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    n = r.Column(r.Integer, nullable=True)
    rpi_id= r.Column(r.Integer, nullable=True)
    threshold = r.Column(r.Integer, nullable=False)
    param0 = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=False)
    alert_state = r.Column(r.Boolean(),unique=False,nullable=False)
    # rlinking - do not have to change the variable name


    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Id":"id",
    "Number":"n",
    "RPi id":"rpi_id",
    "Threshold":"threshold",
    "Param0":"param0",
    "Param1":"param1",
    "Alert?":"alert_state"
    } #header:row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Sensors" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.
    #rlink = {
    #    "rpi_id":("RPi","id")
    #}


    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.n = r.checkNull(insert_list,"n")
        self.rpi_id = r.checkNull(insert_list,"rpi_id")
        self.threshold = insert_list["threshold"]
        self.param0 = insert_list["param0"]
        self.param1 = insert_list["param1"]
        self.alert_state = insert_list["alert_state"]
        #FOR nullable=True, use a the checkNull method
        #self.route_id = r.checkNull(insert_list,"route_id")
