#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Geopath(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Geopath"
    # TODO: DEFINE LIST OF COLUMNS
    name = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False)
    point1_id = r.Column(r.Integer,nullable=False)
    point2_id = r.Column(r.Integer,nullable=False)


    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Geopath number":"id",
    "Pathname":"name",
    "Point 1":"point1_id",
    "Point 2":"point2_id"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Paths" #display for r routes

    # TODO: NOT IMPLEMENT YET, PLEASE IGNORE
    #The following is for r-listing on foreign tables
    rlist_flist = {

    }

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.name = insert_list["name"]
        self.point1_id = insert_list["point1_id"]
        self.point2_id = insert_list["point2_id"]
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class Geopath_AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    rgen_name = r.StringField('New Path',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    rgensel_point1_id = r.SelectField('Point 1',choices=[('0','No point')])
    rgensel_point2_id = r.SelectField('Point 2',choices=[('0','No point')])

    fKeylist = {
    "point1_id":("Geopoint","id"),
    "point2_id":("Geopoint","id")
    }

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class Geopath_EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    rgen_long = r.StringField('Renew Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('Renew Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    rgensel_route_id = r.SelectField('Reassigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}
