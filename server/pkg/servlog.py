#--------------------------------------------------
# servlog.py
# this file contains the logger definition for the loggers
# the will be loaded by packages that require logging
# created 12/12/2018
#--------------------------------------------------

#logging imports
from logging.handlers import RotatingFileHandler
from logging import FileHandler
import logging

from pkg import const
from pkg import limits
import os

flog_standard_format = logging.Formatter(
	'%(name)s--%(asctime)s:%(levelname)s \t[%(message)s]')

#logging declares and setups (REVAMPED AS OF R7, using function for logger generation now)
def attach_Handler(a_loggername,a_handler):
	a_handler.setFormatter(flog_standard_format)
	a_handler.setLevel(logging.INFO)
	out = logging.getLogger(a_loggername)
	out.setLevel(logging.INFO)
	out.addHandler(a_handler)
	return out

def gen_RotatingFileLogger(a_loggername,a_path):
	gen_handler = RotatingFileHandler(a_path, maxBytes=limits.LOGS_MAX_BYTES, backupCount=1)
	return attach_Handler(a_loggername,gen_handler)

def gen_FileLogger(a_loggername,a_path):
	gen_handler = FileHandler(filename=a_path,delay=False)
	return attach_Handler(a_loggername,gen_handler)

#EXPORT THE FOLLOWING
srvlog = {
		"user":gen_FileLogger('user_logger',os.path.join(const.LOGS_DIR,'user.log')),
		"sys":gen_RotatingFileLogger('sys_logger',os.path.join(const.LOGS_DIR,'sys.log')),
		'oper':gen_RotatingFileLogger('ope_logger',os.path.join(const.LOGS_DIR,'oper.log'))
		}

#############################################################################################################
# Referrals
#############################################################################################################
# flog_syslogHandler = RotatingFileHandler(p.path_syslogfileLoc, maxBytes=limits.LOGS_MAX_BYTES, backupCount=1)
# flog_syslogHandler.setFormatter(flog_standard_format)
# flog_syslogHandler.setLevel(logging.INFO)
# flog_syslogger = logging.getLogger('sys_logger')
# flog_syslogger.setLevel(logging.INFO)
# flog_syslogger.addHandler(flog_syslogHandler)
#
# flog_userlogHandler = logging.FileHandler(filename=p.path_userlogfileLoc,delay=False)
# flog_userlogHandler.setFormatter(flog_standard_format)
# flog_userlogHandler.setLevel(logging.INFO)
# flog_userlogger = logging.getLogger('user_logger')
# flog_userlogger.setLevel(logging.INFO)
# flog_userlogger.addHandler(flog_userlogHandler)
