#--------------------------------------------------
# defaults.py
# this file is meant to add default entities onto the database
# for easier development use.
# introduced 8/12/2018
#--------------------------------------------------

from pkg.database.fsqlite import db_session

def default_add():

    #Perma models
    from pkg.database.models import System_User
    from pkg.database.models import System_UserType
    from pkg.database.models import System_Configuration

    #add default values of the configuration table
    #default_config_list = [["ScannerID","AR001"],["MainServerIP","127.0.0.1"],["MainServerPort","4000"]] #used for attemoni
    default_config_list = []
    for configs in default_config_list:
        db_session.add(System_Configuration(configs[0],configs[1]))

    #adding default user - admin
    default_username = "admin"
    default_password = "sha256$mDDYIdTb$9cebe876c8e8fea365c8116a49cc0376ddbb14e03d5043950eb8d8978523fea5"
    default_user = System_User(default_username,default_password,1)
    db_session.add(default_user)

    #adding default userType - admin, seer
    default_utypelist = [["admin",0],["seer",1]]
    for utype in default_utypelist:
        db_session.add(System_UserType(utype[0],utype[1]))

    db_session.commit()
