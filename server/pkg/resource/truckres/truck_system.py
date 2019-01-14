from pkg.resource import res_import as r

class Truck_System(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Truck_System"
    # TODO: DEFINE LIST OF COLUMNS
    long = r.Column(r.Float, nullable=False)
    lati = r.Column(r.Float, nullable=False) #latitude
    reg_no = r.Column(r.String(r.lim.MAX_PASSWORD_SIZE), nullable=False, unique=True)
    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Truck ID":"id",
    "Longitude":"long",
    "Latitude":"lati",
    "Registered Number":"reg_no"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Truck_System" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
        self.reg_no = insert_list["reg_no"]
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class Truck_System_AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_reg_no = r.StringField('New Registered Number',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model

    fKeylist = {}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class Truck_System_EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_long = r.StringField('Renew Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('Renew Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    fKeylist = {}
