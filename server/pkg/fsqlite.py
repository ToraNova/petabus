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
	default_add()
	return

def update_meta():
	#this is called when we want to change our db
	#NOTE please add imports of new models here
	#--------------------------------------------
	from pkg.models import System_User #perma
	from pkg.models import System_Configuration #perma
<<<<<<< HEAD
	from pkg.models import Data_Bus #perma
=======

	from pkg.models import Driver_Register#new

	from pkg.models import Bus_Driver

>>>>>>> ebd74eb02f27f2bdfd02d3c49f43b5bfd7e7973d
	Base.metadata.create_all(bind=engine)

def default_add():
	from pkg.models import System_Configuration #perma
	from pkg.models import System_User #perma
<<<<<<< HEAD
	from pkg.models import Data_Bus #perma
=======

	from pkg.models import Driver_Register #new

	from pkg.models import Bus_Driver

>>>>>>> ebd74eb02f27f2bdfd02d3c49f43b5bfd7e7973d
	#add default values of the configuration table
	#default_config_list = [["ScannerID","AR001"],["MainServerIP","127.0.0.1"],["MainServerPort","4000"]] #used for attemoni
	default_config_list = []
	for configs in default_config_list:
		config_add = System_Configuration(configs[0],configs[1])
		db_session.add(config_add)

	default_username = "admin"
	default_password = "sha256$mDDYIdTb$9cebe876c8e8fea365c8116a49cc0376ddbb14e03d5043950eb8d8978523fea5"
	default_user = System_User(default_username,default_password,True)
	db_session.add(default_user)
	db_session.commit()
