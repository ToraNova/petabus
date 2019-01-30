#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Geopoint(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = __name__
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    long = r.Column(r.Float, nullable=False)
    lati = r.Column(r.Float, nullable=False) #latitude
    route_id = r.Column(r.Integer, nullable=True) #indicate this geopoint belongs to which route

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Geopoint ID":"id",
    "Longitude":"long",
    "Latitude":"lati",
    "Assigned Route ID":"route_id"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Geopoints" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {
        "Assigned Route ID":"Georoute"
    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
        self.route_id = insert_list["route_id"]
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class Geopoint_AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_route_id = r.SelectField('Assigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class Geopoint_EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_long = r.StringField('Renew Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('Renew Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_route_id = r.SelectField('Reassigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}
