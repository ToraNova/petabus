#--------------------------------------------------
# limits.py
# this file serves to hold the important limits
# that are used in the project
# introduced on R2 (pyFlask)
#--------------------------------------------------

################################################################
# Essential Limits (to be used for each pyFlask deployment)
################################################################
MAX_USERNAME_SIZE = 40
MIN_USERNAME_SIZE = 4
MAX_PASSWORD_SIZE = 80 		#sha256 outputs 80 char
MIN_PASSWORD_SIZE = 5
MAX_NAME_SIZE = 50 		#Legal Name
MAX_CONFIG_NAME_SIZE = 50
MAX_CONFIG_VALU_SIZE = 50
LOGS_MAX_BYTES = 100000
TOKEN_LENGTH = 10
################################################################
