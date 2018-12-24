#--------------------------------------------------
# models.py
# this file contains the class definition
# (i.e) the columns are class attributes
# specifically for the database (sqlite3)
# created 8/12/2018
#--------------------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pkg.fsqlite import Base    #fsqlite dependency
from pkg import limits as lim     #lim dependency
from flask_login import UserMixin

class System_User(Base, UserMixin):#This class is permanent in almost all pyFlask deployment
    #System_User is a mandatory class in any pyFlask system
    #This class stores information on the user which will access the system,
    #Examples of instances of this class are admin, user01, human_resource ...
    __tablename__ = "System_User"
    id = Column(Integer, primary_key=True)
    username = Column(String(lim.MAX_USERNAME_SIZE),unique=True,nullable=False)
    password = Column(String(lim.MAX_PASSWORD_SIZE),unique=False,nullable=False)
    adminpri = Column(Boolean(),unique=False,nullable=False)

    def __init__(self,a_username = None,a_password = None,a_adminpri = False):
        self.username = a_username
        self.password = a_password
        self.adminpri = a_adminpri

    def __repr__(self):
        return '<%r %r %r>' % (self.__tablename__,self.username,self.adminpri)

class System_Configuration(Base):#This class is permanent in almost all pyFlask deployment
    #System_Configuration is a mandatory class in any pyFlask system
    #This class stores configurations of the system,
    #Examples of instances of this class are ipaddr, port, server_id ...
    __tablename__ = "System_Config"
    id = Column(Integer,primary_key=True)
    config_name = Column(String(lim.MAX_CONFIG_NAME_SIZE), unique=True,nullable=False)
    config_value = Column(String(lim.MAX_CONFIG_VALU_SIZE), unique=True,nullable=False)

    rlist_col = ["Configuration Name","Configuration Value"] #header
    rlist_dat = ['config_name','config_value'] #row data
    rlist_dis = "Local Configuration" #display

    def __init__(self,a_config_name,a_config_value):
        self.config_name = a_config_name
        self.config_value = a_config_value

    def __repr__(self):
        return '<%r %r>' % (self.__tablename__,self.id)

class Bus_Driver(Base, UserMixin):#This class is permanent in almost all pyFlask deployment
    #System_User is a mandatory class in any pyFlask system
    #This class stores information on the user which will access the system,
    #Examples of instances of this class are admin, user01, human_resource ...
    __tablename__ = "Bus_Driver"
    id = Column(Integer, primary_key=True)
    busname = Column(String(lim.MAX_USERNAME_SIZE),unique=True,nullable=False)
    password = Column(String(lim.MAX_PASSWORD_SIZE),unique=False,nullable=False)

    def __init__(self,a_busname = None,a_password = None):
        self.busname = a_busname
        self.password = a_password

    def __repr__(self):
        return '<%r %r %r>' % (self.__tablename__,self.busname)


###############################################################################
# Non permanent models
#   Regarding non-perma models and is a type of resource (actors/entities)
#   They must take a list in their constructors. PLEASE GO ACCORDING TO SEQUENCE
#   The first element in the list must be the logical identifiable field excluding
#   the intrinsic ID id. All classes MUST have id and another uniquely identifiable ID.
###############################################################################

#NOT USED ON THE LOCAL SITE
# class Class_Scanner(Base):
#     __tablename__ = "Class_Scanner"
#     id = Column(Integer, primary_key=True)
#     csn_id = Column(String(lim.MAX_CLASS_ID), unique=True, nullable=False)#classid is the entity ID.
#     cs_label = Column(String(lim.MAX_CLASS_LABEL),unique=False,nullable=False)#Where is the class conducted ?
#
#     #The following is for r-listing (resource listing)
#     rlist_col = ["Scanner ID","Label"] #header
#     rlist_dat = ['csn_id','cs_label'] #row data
#     rlist_dis = "RFID Scanner List" #display
#
#     def __init__(self,insert_list):
#         self.csn_id = insert_list['csn_id']
#         self.cs_label = insert_list['cs_label']
#
#     def __repr__(self):
#     	return '<%r %r>' % (self.__tablename__,self.id)
#
#     priKey = 0 #rlist_dat[0] is the primary key :default

# TODO implement the following.
# class Class_Session(Base):
#     __tablename__ = "Class_Session"
#     id = Column(Integer, primary_key=True)
#     c_id = Column(String(lim.MAX_CLASS_ID), unique=True, nullable=False)#classid is the entity ID.
#     c_label = Column(String(lim.MAX_CLASS_LABEL),unique=False,nullable=False)#Name of class ?
#     csn_id = Column(String(lim.MAX_CLASS_ID), unique=False, nullable=False)#Foreign key that links to class_scanner
#     c_start = Column(DateTime())
#     c_end = Column(DateTime())
#     def __init__(self,a_classid,a_classlabel = None,a_csn_id,a_c_start,a_c_end):
#         self.c_id = a_classid
#         self.c_label = a_classlabel
#         self.csn_id = a_csn_id
#         self.c_start = a_c_start
#         self.c_end = a_c_end
#
#     def __repr__(self):
#     	return '<%r %r>' % (self.__tablename__,self.id)
#
# class Class_Registration(Base): #Implements M:N relationship between student & class_session
#     __tablename__ = "Class_Registration"
#     id = Column(Integer, primary_key=True)
#     c_id = Column(String(lim.MAX_CLASS_ID), unique=True, nullable=False)#classid is the entity ID.
#     s_id = Column(String(lim.MAX_STUDENT_ID),unique=True,nullable=False)#studentid is the entity ID
#     def __init__(self,a_c_id,a_s_id):
#         self.c_id = a_c_id
#         self.s_id = a_s_id
#
#     def __repr__(self):
#     	return '<%r %r>' % (self.__tablename__,self.id)

# class Attendance(Base): #Attendance data. records s_id, csn_id, datetime and c_id
#    __tablename__ = "Attendance"
#    id = Column(Integer,primary_key=True)
#    s_id = Column(String(lim.MAX_STUDENT_ID),unique=False,nullable=False)
#    csn_id = Column(String(lim.MAX_CLASS_ID), unique=False, nullable=False)
#    scan_time = Column(DateTime(),nullable=False)

    #The following is for d-listing (data listing)
#    dlist_col = ["uid","Student ID","Scanner ID","Scanning Time"]
#    dlist_dat = ['id','s_id','csn_id','scan_time']
#
#    #rlist compatibility #TODO, independent compat.
#    rlist_col = dlist_col
#    rlist_dat = dlist_dat #FOR getMatch under pkg.fdist
#
#    def __init__(self,a_s_id,a_csn_id,a_scan):
#        self.s_id = a_s_id
#        self.csn_id = a_csn_id
#        self.scan_time = a_scan
#
#    def __repr__(self):
#        return '<%r %r>' % (self.__tablename__,self.id)

#NOT USED ON THE LOCAL SITE
# class Student(Base):
#     __tablename__ = "Student"
#     id = Column(Integer, primary_key=True)
#     s_id = Column(String(lim.MAX_STUDENT_ID),unique=True,nullable=False)#studentid is the entity ID
#     s_name = Column(String(lim.MAX_NAME_SIZE),nullable=False)
#
#     #The following is for r-listing (resource listing)
#     rlist_col = ["Student ID","Student Name"] #header
#     rlist_dat = ['s_id','s_name'] #row data
#     rlist_dis = "Student Database" #display
#     def __init__(self,insert_list):
#         self.s_id = insert_list['s_id']
#         self.s_name = insert_list['s_name']
#
#     def __repr__(self):
#         return '<%r %r>' % (self.__tablename__,self.id)
#
#     priKey = 0 #rlist_dat[0] is the primary key :default
