#!/usr/bin/python3

#--------------------------------------------------
# server.py
# this is the main file to be executed
# created 8/12/2018
#--------------------------------------------------

#from pkg.fsock import fsock_app #re-import the app after routing and socketing
from pkg.source import server
from pkg.system.servlog import srvlog

from pkg.database.fsqlite import init_db
from pkg.database.fsqlite import db_session

import os.path

main_host = '0.0.0.0'
main_port = 8000
main_debug = True
app_debug = True

#First run issues (create database)
try:
    if(not os.path.isfile("init.token")):
        #database not initialized yet
        tokenfile = open("init.token","w+")
        tokenfile.close()
        init_db()#initialization
    else:
        print("[IF]",__name__," : ","Database already initialized...skipping")
        pass
except  Exception as e:
    print("[ER]",__name__," : ","Exception occured while trying to create database")
    print (e)

if __name__ == '__main__':

    petabus = server()
    srvlog["sys"].info("system start") #logging
    try:
        #fsock_app.run(routed_app,debug=app_debug,host=main_host, port=main_port, use_reloader = False) #FlaskIO run
        petabus.run(debug=app_debug,host=main_host, port=main_port, use_reloader = True,threaded=True)
    except Exception as e:
        print("Exception error",e)
        srvlog["sys"].error("exception error")
        srvlog["sys"].error(e)
    finally:
        print("[IF] Server terminated.")
        srvlog["sys"].info("system halt") #logging
