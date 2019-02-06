#--------------------------------------------------
# georoute.py
# Georotue is a model for a route on a map
# this model is currently relatively simple, having only
# a route name.
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class Georoute(r.Base):
    __tablename__ = "Georoute"
    id = r.Column(r.Integer, primary_key=True)
    name = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=True) #longitude

    #The following is for r-listing (resource listing)
    rlist = {
    "Georoute ID":"id",
    "Georoute Name":"name",
    } #header:row data

    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Georoutes" #display for r routes

    def __init__(self,insert_list):
        self.name = insert_list["name"]

    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)

    def getselfname(self):
        return self.__class__.__name__

# Anything after rgen_ must be an actual attribute from Georoute
class AddForm(r.FlaskForm):
    rgen_name = r.StringField('New Georoute Name',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_USERNAME_SIZE)])
    fKeylist = {}

class EditForm(r.FlaskForm):
    rgen_name = r.StringField('Renew Georoute Name',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_USERNAME_SIZE)])
    fKeylist = {}
