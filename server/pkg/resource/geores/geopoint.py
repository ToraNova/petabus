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
    time = r.Column(r.DateTime, nullable=False)

    # rlinking - do not have to change the variable name
    route_id = r.Column(r.Integer, nullable=True)

    #The following is for r-listing (resource listing)
    rlist = {
    "Geopoint ID":"id",
    "Longitude":"long",
    "Latitude":"lati",
    "Linked Route":"__link__/route_id", # __link__/ is a reserved keyword
    "Timestamp":"time"
    } #header:row data
    #
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Geopoints" #display for r routes

    #rlink - ref tablename, fkey, lookup
    rlink = {
        "route_id":("Georoute","id","name")
    }

    def __init__(self,insert_list):
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
        self.time = insert_list["time"]

        #FOR nullable=True, use a the checkNull method
        self.route_id = r.checkNull(insert_list,"route_id")

    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)

class AddForm(r.FlaskForm):
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgensel_route_id = r.SelectField('Assigned Route',choices=[('0','No link')])
    rgentim_time = r.DateField('T stamp', widget=r.DatePickerWidget(),default=r.datetime.datetime.now())
    fKeylist = {"route_id":("Georoute","name")}

class EditForm(r.FlaskForm):
    rgen_long = r.StringField('Renew Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('Renew Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgensel_route_id = r.SelectField('Reassigned Route',choices=[('0','No link')])
    #rgentim_time = r.DateField('New T-stamp', widget=r.DatePickerWidget(),default=r.datetime.datetime.now())
    fKeylist = {"route_id":("Georoute","name")}
