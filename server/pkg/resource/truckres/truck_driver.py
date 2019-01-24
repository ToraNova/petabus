#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Truck_Driver(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Truck_Driver"
    # TODO: DEFINE LIST OF COLUMNS
    name = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=False)
    contact_no = r.Column(r.String(r.lim.MAX_CONTACT_SIZE), nullable=False, unique=True) #longitude
    password = r.Column(r.String(r.lim.MAX_PASSWORD_SIZE),unique=False,nullable=False)
    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Driver ID":"id",
    "Driver Name":"name",
    "Contact Number":"contact_no"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Truck_Driver" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.name = insert_list["name"]
        self.contact_no = insert_list["contact_no"]
        self.password = insert_list["password"]
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class Truck_Driver_AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_name = r.StringField('New Name',validators=[r.InputRequired(),r.Length(min=4,max=40)])
    rgen_contact_no = r.StringField('New Contact Number',validators=[r.InputRequired(),r.Length(min=10,max=11)])
    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_password = r.PasswordField('New Password',validators=[r.InputRequired(),r.Length(min=5,max=80)])
    fKeylist = {}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class Truck_Driver_EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_name = r.StringField('Renew Name',validators=[r.InputRequired(),r.Length(min=4,max=40)])
    rgen_contact_no = r.StringField('Renew Contact Number',validators=[r.InputRequired(),r.Length(min=10,max=11)])
    #rgen_password = r.PasswordField('New Password',validators=[r.InputRequired(),r.Length(min=5,max=80)])
    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    fKeylist = {}
