#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Bus(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Bus"
    # TODO: DEFINE LIST OF COLUMNS
    reg_no = r.Column(r.String(r.lim.MAX_PASSWORD_SIZE), nullable=False, unique=True)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Bus ID":"id",
    "Registered Number":"reg_no"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Bus" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.reg_no = insert_list["reg_no"]

    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class Bus_AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_reg_no = r.StringField('New Registered Number',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model

    fKeylist = {}
