#--------------------------------------------------
# fsqlite.py
# this file is static and should not be tampered with
# it initializes the required models for the database engine
# introduced 8/12/2018
#--------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pkg.const as const
import os

#configuration necessities
#fixed prefix on database filename : 'sqlite:///<filename>'
#3 slashes are necessary
engine = create_engine('sqlite:///'+const.DB00_NAME,convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	#call this during first init
	update_meta()

	from pkg.database.defaults import default_add
	default_add()
	tokenfile = open(os.path.join(const.TOKN_DIR,"init.token"),"w+")
	tokenfile.close()
	return

def update_meta():
	#this is called when we want to change our db
	#NOTE please add imports of new models here
	#-----------------------PERMA MODELS-------------------------------------
	from pkg.database.models import System_User #perma
	from pkg.database.models import System_Configuration #perma
	#------------------------------------------------------------------------

	#-----------------------Non PERMA----------------------------------------
	from pkg.resource import rdef
	#------------------------------------------------------------------------

	Base.metadata.create_all(bind=engine)
