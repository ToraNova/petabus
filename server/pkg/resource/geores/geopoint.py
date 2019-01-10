#--------------------------------------------------
# geopoint.py
# Geopoint is a model that consist of a longitude
# and a latitude. likewise, a uuid is also available
# to aid routing, a route id is also here to help link
# a point to a route. (this is still under dev)
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Geopoint(r.Base):
    __tablename__ = "Geopoint"
    id = r.Column(r.Integer, primary_key=True)
    long = r.Column(r.Float, nullable=False) #longitude
    lati = r.Column(r.Float, nullable=False) #latitude
    route_id = r.Column(r.Integer, nullable=True) #indicate this geopoint belongs to which route

    #The following is for r-listing (resource listing)
    rlist = {
    "Geopoint ID":"id",
    "Longitude":"long",
    "Latitude":"lati",
    "Assigned Route ID":"route_id"
    } #header:row data
    #
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Geopoints" #display for r routes

    #The following is for r-listing on foreign tables
    rlist_flist = {
        "Assigned Route ID":"Georoute"
    }

    def __init__(self,insert_list):
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
        self.route_id = insert_list["route_id"]

    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)

class Geopoint_AddForm(r.FlaskForm):
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgensel_route_id = r.SelectField('Assigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}

class Geopoint_EditForm(r.FlaskForm):
    rgen_long = r.StringField('Renew Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('Renew Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgensel_route_id = r.SelectField('Reassigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}
